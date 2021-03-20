## Description
Try to recover the flag stored on this website http://mercury.picoctf.net:2148/

### Hints
- The flag is at ../flag

## Tools I Used
- None

## Thought Process
`../` means traversing one directory up so the hint pretty much gave it away that it is a path traversal problem.

\
The most intuitive approach is to just directly add `../flag` to the url, so I typed `http://mercury.picoctf.net:2148/../flag` into the browser.
Guess what... of course the problem isn't that simple! It automatically filtered my path to become `http://mercury.picoctf.net:2148/flag` and responded with a `404 Not Found` page.

\
Welp, now I was ready to try a couple other path traversal methods, with the first being trying the URL-encoded version of `../`, which is `%2E%2E%2F`. The idea behind this is that if the server only searches for `../`, they will not be able to filter out the URL encoding version. So I typed `http://mercury.picoctf.net:2148/%2E%2E%2Fflag` into the browser and ... bamn! It worked and we got the flag!

I guess I no longer need to try the more annoying methods : )

## Flag
`picoCTF{th15_vu1n_1s_5up3r_53r1ous_y4ll_8db8f85c}`