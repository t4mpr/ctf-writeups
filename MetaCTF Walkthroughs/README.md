# MetaCTF — Walkthroughs


---

## Challenges
**I've Got The Magic**

![Magic In Me](images/Magic_In_me.png)
File provided: [`magicinme`](files/magicinme)

>by typing `file magicinme` into our termianl - we discover the file type without the file having the correct extention. (i.e .7z or .zip)
\
>We then change add the correct extention to the file `mv magicinme magicinme.7z`
 ![Magic In Me 1](images/Magic_In_Me_1.png)
>>Then, we unzip with `7z e magicinme.7z`
![Magic In Me 2](images/Magic_In_Me_2.png)
>>>open the file with `xdg-open flag.jpg`
![Magic In Me 3](images/Magic_In_Me_3.png)
>>>>Retrieve the flag
![magic_in_me_flag](images/flag.jpg)

**Forensics, Here I Come**

![Here I Come](images/Here_I_come_.png)

`xxd -l 2 [filename]`

Breakdown of the command:
- xxd: Creates a hex dump of a file.
- -l 2: Limits the output to the first 2 bytes.
- [filename]: The file you want to examine.

Example output for a Windows executable:
![Here I Come 1](images/Here_I_come_1.png)




---


See you next time!

-[t4mpr](https://linkedin.com/in/smosillo)




