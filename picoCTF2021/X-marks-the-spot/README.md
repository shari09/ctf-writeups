## Description
Another login you have to bypass. Maybe you can find an injection that works? http://mercury.picoctf.net:7029/

### Hints
- XPATH

## Tools I Used
- Chrome developer tools
- Python (requests lib)

## Thought Process
Using the hint, it was obvious that this was a [xpath injection problem](https://owasp.org/www-community/attacks/XPATH_Injection).



The xpath query was probably something along the lines of
```
//user[name/text()='{userInputUser}' and pass/text()='{userInputPass}']
```
Of course we didn't know if the path was `//user` or if the nodes were `name` or `pass`. However, I used those values for testing on http://xpather.com/ with my own xml document.


## Flag
`picoCTF{k3ep_1t_sh0rt_6fdd78c92c7f26a10acd3ece176dea4d}`