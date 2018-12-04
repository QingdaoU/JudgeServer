package judge

import (
	"net/http"
	"io/ioutil"
	"io"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"time"
	"bytes"
	"fmt"
)

type Resp struct {
	RespData interface{} `json:"data"`
	RespErr  string      `json:"err"`
	err      error       `json:"-"`
}

func (resp *Resp) Data() interface{} {
	if resp == nil {
		return nil
	}
	return resp.RespData
}

func (resp *Resp) Err() error {
	if resp == nil {
		return nil
	}
	return resp.err
}

func parseResp(body []byte) (*Resp, error) {
	resp := &Resp{}
	err := json.Unmarshal(body, resp)
	if err != nil {
		return nil, err
	}
	// 有错误的响应了
	if resp.RespErr != "" {
		resp.err = fmt.Errorf("err: %s, data: %s", resp.RespErr, resp.RespData)
	}

	return resp, nil
}

type Client struct {
	opts        *options
	sha256Token string
	httpClient  *http.Client
}

func (c *Client) request(method, path string, body io.Reader) (resp *Resp, err error) {
	req, err := http.NewRequest("POST", c.opts.EndpointURL+"/"+path, body)
	if err != nil {
		return
	}
	req.Header.Set("X-Judge-Server-Token", c.sha256Token)
	req.Header.Set("Content-Type", "application/json")

	httpResp, err := c.httpClient.Do(req)
	if err != nil {
		return
	}
	b, err := ioutil.ReadAll(httpResp.Body)
	if err != nil {
		return
	}
	httpResp.Body.Close()
	return parseResp(b)
}

func (c *Client) post(path string, body io.Reader) (resp *Resp, err error) {
	return c.request("POST", path, body)
}

// Ping Judge server
func (c *Client) Ping() (resp *Resp, err error) {
	resp, err = c.post("ping", nil)
	return
}

func (c *Client) CompileSpj(src, spjVersion string, spjCompileConfig *CompileConfig) (resp *Resp, err error) {
	data := map[string]interface{}{
		"src":                src,
		"spj_version":        spjVersion,
		"spj_compile_config": spjCompileConfig,
	}
	b, err := json.Marshal(data)
	if err != nil {
		return
	}
	resp, err = c.post("compile_spj", bytes.NewReader(b))
	return
}

func New(endpointURL, token string, timeout time.Duration) *Client {
	return NewClient(
		WithEndpointURL(endpointURL),
		WithToken(token),
		WithTimeout(timeout),
	)
}

func NewClient(options ...Option) *Client {
	opts := DefaultOptions
	for _, o := range options {
		o(opts)
	}
	sha256Token := sha256.Sum256([]byte(opts.Token))
	return &Client{
		opts:        opts,
		sha256Token: hex.EncodeToString(sha256Token[:]),
		httpClient: &http.Client{
			Timeout: opts.Timeout,
		},
	}
}
