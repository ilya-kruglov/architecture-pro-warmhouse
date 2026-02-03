package services

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

type TelemetryClient struct {
	BaseURL    string
	HTTPClient *http.Client
}

type TelemetryData struct {
	DeviceID   string    `json:"device_id"`
	MetricType string    `json:"metric_type"`
	Value      float64   `json:"value"`
	Unit       string    `json:"unit"`
	Timestamp  time.Time `json:"timestamp"`
}

func NewTelemetryClient(baseURL string) *TelemetryClient {
	return &TelemetryClient{
		BaseURL: baseURL,
		HTTPClient: &http.Client{
			Timeout: 10 * time.Second,
		},
	}
}

func (c *TelemetryClient) AddTelemetry(deviceID, metricType string, value float64, unit string) error {
	url := fmt.Sprintf("%s/telemetry", c.BaseURL)
	
	requestBody := map[string]interface{}{
		"device_id":   deviceID,
		"metric_type": metricType,
		"value":       value,
		"unit":        unit,
	}
	
	jsonBody, _ := json.Marshal(requestBody)
	
	resp, err := c.HTTPClient.Post(url, "application/json", bytes.NewBuffer(jsonBody))
	if err != nil {
		return fmt.Errorf("error adding telemetry: %w", err)
	}
	defer resp.Body.Close()
	
	if resp.StatusCode != http.StatusOK && resp.StatusCode != http.StatusCreated {
		return fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}
	
	return nil
}

func (c *TelemetryClient) GetTelemetry(deviceID string) ([]TelemetryData, error) {
	url := fmt.Sprintf("%s/telemetry?device_id=%s", c.BaseURL, deviceID)
	
	resp, err := c.HTTPClient.Get(url)
	if err != nil {
		return nil, fmt.Errorf("error fetching telemetry: %w", err)
	}
	defer resp.Body.Close()
	
	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}
	
	var telemetry []TelemetryData
	if err := json.NewDecoder(resp.Body).Decode(&telemetry); err != nil {
		return nil, fmt.Errorf("error decoding telemetry response: %w", err)
	}
	
	return telemetry, nil
}