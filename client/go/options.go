package judge

import "time"

type options struct {
	// scheme://host:port .
	EndpointURL string
	Token       string
	// 请求超时时间
	// 如果 Timeout 为 0，那么意味着不会超时
	Timeout time.Duration
}

var DefaultOptions = &options{
	EndpointURL: "http://127.0.0.1:12358",
	Token:       "YOUR_TOKEN_HERE",
	Timeout:     10 * time.Second,
}

type Option func(*options)

func WithEndpointURL(u string) Option {
	return func(o *options) {
		o.EndpointURL = u
	}
}

func WithToken(token string) Option {
	return func(o *options) {
		o.Token = token
	}
}

func WithTimeout(timeout time.Duration) Option {
	return func(o *options) {
		o.Timeout = timeout
	}
}
