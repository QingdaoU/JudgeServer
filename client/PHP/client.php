<?php

Class JudgeClient{

    private $ch = null;
    private $serverBaseUrl = '';

    public function __construct($token, $serverBaseUrl)
    {
        $this->serverBaseUrl = rtrim($serverBaseUrl, '/');
        $this->ch = curl_init();
        $defaults = [
            CURLOPT_RETURNTRANSFER  =>  1,
            CURLOPT_HEADER          =>  0,
            CURLOPT_HTTPHEADER      =>  [
                'Content-type: text/json',
                'X-Judge-Server-Token: '.$token
            ],
            //POST方式
            CURLOPT_POST            =>  1
        ];
        curl_setopt_array($this->ch, $defaults);
    }

    /**
     * 发送http请求
     * @param $url  请求的url
     * @param $data 请求参数
     */
    private function request($url, $data = []){
        curl_setopt($this->ch, CURLOPT_URL, $url);
        curl_setopt($this->ch, CURLOPT_POSTFIELDS, empty($data)?'{}':json_encode($data));
        if( ! $result = curl_exec($this->ch))
        {
            trigger_error(curl_error($this->ch));
        }
        return $result;
    }
    public function ping(){
        return $this->request($this->serverBaseUrl.'/ping');
    }

    public function judge($src, $language_config, $max_cpu_time, $max_memory, $test_case_id, $output = false, $spj_version = null,
                          $spj_config = null, $spj_compile_config = null, $spj_src = null){
        $data = [
            'language_config'       =>  $language_config,
            'src'                   =>  $src,
            'max_cpu_time'          =>  $max_cpu_time,
            'max_memory'            =>  $max_memory,
            'test_case_id'          =>  $test_case_id,
            'spj_version'           =>  $spj_version,
            'spj_config'            =>  $spj_config,
            'spj_compile_config'    =>  $spj_compile_config,
            'spj_src'               =>  $spj_src,
            'output'                =>  $output
        ];
        return $this->request($this->serverBaseUrl.'/judge', $data);

    }
    public function compileSpj($src, $spj_version, $spj_compile_config, $test_case_id){
        $data = [
            'src'                   =>  $src,
            'spj_version'           =>  $spj_version,
            'spj_compile_config'    =>  $spj_compile_config,
            'test_case_id'          =>  $test_case_id
        ];
        return $this->request($this->serverBaseUrl.'/compile_spj', $data);
    }
    public function close(){
        if( is_resource($this->ch) ){
            curl_close( $this->ch );
        }
    }

    public function __destruct()
    {
        $this->close();
    }
}


$c_src = <<<EOD
#include <stdio.h>
int main(){
    int a, b;
    scanf("%d%d", &a, &b);
    printf("%d", a+b);
    return 0;
}
EOD;

$c_spj_src = <<<EOD
#include <stdio.h>
int main(){
    return 1;
}
EOD;

$cpp_src = <<<EOD
#include <iostream>

using namespace std;

int main()
{
    int a,b;
    cin >> a >> b;
    cout << a+b << endl;
    return 0;
}
EOD;
$java_src = <<<EOD
import java.util.Scanner;
public class Main{
    public static void main(String[] args){
        Scanner in=new Scanner(System.in);
        int a=in.nextInt();
        int b=in.nextInt();
        System.out.println(a + b);
    }
}
EOD;

$py2_src = <<<EOD
s = raw_input()
s1 = s.split(" ")
print int(s1[0]) + int(s1[1])
EOD;

$js_src = 'console.log(3)';

$judgeClient = new JudgeClient(hash('sha256', 'token'), 'http://123.57.151.42:12358');
$languages = require('languages.php');

echo "ping:\n";
print_r(json_decode($judgeClient->ping()));

echo "\n\ncompile_spj:\n";
print_r(json_decode($judgeClient->compileSpj($c_spj_src, '2',$languages['c_lang_spj_compile'], 'spj')));

echo "\n\njudge c:\n";
print_r(json_decode($judgeClient->judge($c_src, $languages['c_lang_config'], 1000, 1024 * 1024 * 128, 'normal', true)));

echo "\n\njudge cpp:\n";
print_r(json_decode($judgeClient->judge($cpp_src, $languages['cpp_lang_config'], 1000, 1024 * 1024 * 128, 'normal')));

echo "\n\njudge java:\n";
print_r(json_decode($judgeClient->judge($java_src, $languages['java_lang_config'], 1000, 1024 * 1024 * 128, 'normal')));

echo "\n\njudge python2:\n";
print_r(json_decode($judgeClient->judge($py2_src, $languages['py2_lang_config'], 1000, 1024 * 1024 * 128, 'normal')));
