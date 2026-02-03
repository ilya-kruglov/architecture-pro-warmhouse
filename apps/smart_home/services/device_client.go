package services

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

type DeviceClient struct {
	BaseURL    string
	HTTPClient *http.Client
}

type Device struct {
	DeviceID   string                 `json:"device_id"`
	Name       string                 `json:"name"`
	DeviceType string                 `json:"device_type"`
	Location   string                 `json:"location"`
	Status     string                 `json:"status"`
	Metadata   map[string]interface{} `json:"metadata"`
	CreatedAt  time.Time              `json:"created_at"`
	LastSeen   *time.Time             `json:"last_seen"`
}

func NewDeviceClient(baseURL string) *DeviceClient {
	return &DeviceClient{
		BaseURL: baseURL,
		HTTPClient: &http.Client{
			Timeout: 10 * time.Second,
		},
	}
}

func (c *DeviceClient) GetDevice(deviceID string) (*Device, error) {
	url := fmt.Sprintf("%s/devices/%s", c.BaseURL, deviceID)
	
	resp, err := c.HTTPClient.Get(url)
	if err != nil {
		return nil, fmt.Errorf("error fetching device: %w", err)
	}
	defer resp.Body.Close()
	
	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}
	
	var device Device
	if err := json.NewDecoder(resp.Body).Decode(&device); err != nil {
		return nil, fmt.Errorf("error decoding device response: %w", err)
	}
	
	return &device, nil
}

func (c *DeviceClient) CreateDevice(name, deviceType, location string) (*Device, error) {
	url := fmt.Sprintf("%s/devices", c.BaseURL)
	
	requestBody := map[string]interface{}{
		"name":        name,
		"device_type": deviceType,
		"location":    location,
	}
	
	jsonBody, _ := json.Marshal(requestBody)
	
	resp, err := c.HTTPClient.Post(url, "application/json", bytes.NewBuffer(jsonBody))
	if err != nil {
		return nil, fmt.Errorf("error creating device: %w", err)
	}
	defer resp.Body.Close()
	
	if resp.StatusCode != http.StatusCreated {
		return nil, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}
	
	var device Device
	if err := json.NewDecoder(resp.Body).Decode(&device); err != nil {
		return nil, fmt.Errorf("error decoding device response: %w", err)
	}
	
	return &device, nil
}