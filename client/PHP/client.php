<?php

require('JudgeClient.php');

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


$judgeClient = new JudgeClient(hash('sha256', 'token'), 'http://123.57.151.42:12358');
$languages = require('languages.php');

echo "ping:\n";
print_r($judgeClient->ping());

echo "\n\ncompile_spj:\n";
print_r($judgeClient->compileSpj($c_spj_src, '2', $languages['c_lang_spj_compile'], 'spj'));

echo "\n\njudge c:\n";
print_r($judgeClient->judge($c_src, $languages['c_lang_config'], 1000, 1024 * 1024 * 128, 'normal', true));

echo "\n\njudge cpp:\n";
print_r($judgeClient->judge($cpp_src, $languages['cpp_lang_config'], 1000, 1024 * 1024 * 128, 'normal'));

echo "\n\njudge java:\n";
print_r($judgeClient->judge($java_src, $languages['java_lang_config'], 1000, 1024 * 1024 * 128, 'normal'));

echo "\n\njudge python2:\n";
print_r($judgeClient->judge($py2_src, $languages['py2_lang_config'], 1000, 1024 * 1024 * 128, 'normal'));
