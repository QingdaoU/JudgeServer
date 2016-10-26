<?php


class JudgeClient
{

    private $ch = null;
    private $serverBaseUrl = '';

    public function __construct($token, $serverBaseUrl)
    {
        $this->serverBaseUrl = rtrim($serverBaseUrl, '/');
        $this->ch = curl_init();
        $defaults = [
            CURLOPT_RETURNTRANSFER => 1,
            CURLOPT_HEADER => 0,
            CURLOPT_HTTPHEADER => [
                'Content-type: application/json',
                'X-Judge-Server-Token: ' . $token
            ],
            //POST方式
            CURLOPT_POST => 1
        ];
        curl_setopt_array($this->ch, $defaults);
    }

    /**
     * 发送http请求
     * @param $url string 请求的url
     * @param $data array 请求参数
     */
    private function request($url, $data = [])
    {
        curl_setopt($this->ch, CURLOPT_URL, $url);
        curl_setopt($this->ch, CURLOPT_POSTFIELDS, empty($data) ? '{}' : json_encode($data));
        if (!$result = curl_exec($this->ch)) {
            trigger_error(curl_error($this->ch));
        }
        return json_decode($result);
    }

    public function ping()
    {
        return $this->request($this->serverBaseUrl . '/ping');
    }

    public function judge($src, $language_config, $max_cpu_time, $max_memory, $test_case_id, $output = false, $spj_version = null,
                          $spj_config = null, $spj_compile_config = null, $spj_src = null)
    {
        $data = [
            'language_config' => $language_config,
            'src' => $src,
            'max_cpu_time' => $max_cpu_time,
            'max_memory' => $max_memory,
            'test_case_id' => $test_case_id,
            'spj_version' => $spj_version,
            'spj_config' => $spj_config,
            'spj_compile_config' => $spj_compile_config,
            'spj_src' => $spj_src,
            'output' => $output
        ];
        return $this->request($this->serverBaseUrl . '/judge', $data);

    }

    public function compileSpj($src, $spj_version, $spj_compile_config, $test_case_id)
    {
        $data = [
            'src' => $src,
            'spj_version' => $spj_version,
            'spj_compile_config' => $spj_compile_config,
            'test_case_id' => $test_case_id
        ];
        return $this->request($this->serverBaseUrl . '/compile_spj', $data);
    }

    public function close()
    {
        if (is_resource($this->ch)) {
            curl_close($this->ch);
        }
    }

    public function __destruct()
    {
        $this->close();
    }
}
