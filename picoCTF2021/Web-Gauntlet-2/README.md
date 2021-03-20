## Description
This website looks familiar... Log in as admin Site: http://mercury.picoctf.net:65261/ Filter: http://mercury.picoctf.net:65261/filter.php

### Hints
- I tried to make it a little bit less contrived since the mini competition.
- Each filter is separated by a space. Spaces are not filtered.
- There is only 1 round this time, when you beat it the flag will be in filter.php.
- There is a length component now.
- sqlite

## Tools I Used
- None

## Thought Process
The hints were apparently referring to `Web Gauntlet 1` from the mini 2020 picoCTF, which I didn't participate in, so I was *really* confused on what they were supposed to mean. The only things I got out of the hints were that:
-  It's a SQL injection problem and uses SQLite DBMS.
-  If I solve it right, the flag is at http://mercury.picoctf.net:65261/filter.phpp and not http://mercury.picoctf.net:65261/index.php so I won't go on a wild goose chase in the future.

\
Navigating to the `filter.php` page, I saw `Filters: or and true false union like = > < ; -- /* */ admin`, which were all SQL commands, so I was definitely sure this was just a SQL injection challenge.

\
I tried a random username and password combo for starting:
```
username: hello
password: hi
```
and of course, it gave me a `not admin` error. However, I noticed there was something at the top of the page: `SELECT username, password FROM users WHERE username='hello' AND password='hi'`. That was probably the query they were using to check whether or not I was admin.

\
The `not admin` error message combined with the `admin` in the filter.php, I had a pretty good feeling that the correct username is just `admin`. We could easily bypass the filter using string concatenation, which was done via `||` in SQLite, so the query would look something like `...WHERE username='admi'||'n' AND...`, with the injection being `admi'||'n`.

Since `or` and `=` are both filtered, I couldn't just inject something like `a' or '1'='1` into the password field. So I was thinking that the only way we could do it would be getting the actual password to satisfy the `password=` query. That can be done through the use of a sub-query and concatenation for the password field. The query would look like `password=''|| (SELECT password FROM users WHERE username='admi'||'n') ||''`.

Expected query:
```
SELECT username, password FROM users WHERE username='admi'||'n' AND password=''|| (SELECT password FROM users WHERE username='admi'||'n') ||''
```

Injection:
```
username: admi'||'n
password: '|| (SELECT password FROM users WHERE username='admi'||'n') ||'
```


So I typed that and... oof, it gave me an error saying `Combined input lengths too long! (> 35)` : /

\
Oh well, with a 35chars limit, there was no way I could query for the actual password since the column names (`username`, `password`) were already 16 characters, and the query statements were ~5char each. After staring at their query statement for long time, it occurred to me that "why don't I just insert an extra single quote at the `username` injection to invalidate the entire password checking part?"

The query they were using is\
`SELECT username, password FROM users WHERE username='{username_injection}' AND password='{password_injection}'`
So if I did something like\
<code>SELECT username, password FROM users WHERE username=<mark>'admi'</mark>||<mark>'n'</mark>||<mark>' AND password='</mark>||<mark>''</mark></code>
The entire `AND password=` was just a part of the username now. However, I needed to trim that part off since the username should just be `admin`, so I used the `substr(string,position,length)` provided by SQLite.

Final query\
<code>SELECT username, password FROM users WHERE username=<mark>'admi'</mark>||<mark>'n'</mark>||<mark>substr(' AND password=',0,0)</mark>||<mark>''</mark></code>

Injection:
```
username: admi'||'n'||substr(
password: ,0,0)||'
```
totalling 27 characters

\
It gave me the response of `Congrats! You won! Check out filter.php`. So I navigated there, refreshed, and saw the flag.


## Flag
`picoCTF{0n3_m0r3_t1m3_e2db86ae880862ad471aa4c93343b2bf}`