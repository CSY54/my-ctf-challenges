# [Reverse] ⒸⓄⓋⒾⒹ-①⑨

- Points: 371
- Difficulty: ★
- Solves: 14/190 (MyFirstCTF)
- Keywords: Baby

## Descriptions

Destroy Corona!

Author: CSY54

## Writeup

**TL;DR**

1. 把 [task](release/task) 丟進 Decompiler
2. 逆向 `check_flag_is_correct()`



**`objdump` 解**

用 `objdump` dump 出該 object file 中的資訊後可以發現在 `main()` 中呼叫了一個叫做 `_Z21check_flag_is_correctPc()` 的 function。

觀察 `_Z21check_flag_is_correctPc` 的內容可以知道他把傳入的參數當作一個長度為 0x19 的陣列，並將陣列中第 `i` 個值與 `i` xor 起來（`a[i] ^ i`），再拿去跟 `target` 中的第 `i` 個值比較（`target[i]`），當比較全部正確後會回傳 1，否則回傳 0。

```shell
$ objdump -M intel -d task

task:     file format elf64-x86-64

Disassembly of section .text:

0000000000001389 <_Z21check_flag_is_correctPc>:
    1389:	f3 0f 1e fa          	endbr64
    138d:	b8 00 00 00 00       	mov    eax,0x0
    1392:	b9 01 00 00 00       	mov    ecx,0x1
    1397:	4c 8d 05 72 2c 00 00 	lea    r8,[rip+0x2c72]        # 4010 <target>
    139e:	0f be 14 07          	movsx  edx,BYTE PTR [rdi+rax*1]
    13a2:	31 c2                	xor    edx,eax
    13a4:	41 0f be 34 00       	movsx  esi,BYTE PTR [r8+rax*1]
    13a9:	39 f2                	cmp    edx,esi
    13ab:	0f 94 c2             	sete   dl
    13ae:	0f b6 d2             	movzx  edx,dl
    13b1:	21 d1                	and    ecx,edx
    13b3:	48 83 c0 01          	add    rax,0x1
    13b7:	48 83 f8 19          	cmp    rax,0x19
    13bb:	75 e1                	jne    139e <_Z21check_flag_is_correctPc+0x15>
    13bd:	89 c8                	mov    eax,ecx
    13bf:	c3                   	ret
    
00000000000013c0 <main>:
	  ...
    16cd:	48 89 e7             	mov    rdi,rsp
    16d0:	e8 b4 fc ff ff       	call   1389 <_Z21check_flag_is_correctPc>
	  ...
```

接下來可以用 `readelf` 取出 `target` 的內容，然後想辦法讓 `_Z21check_flag_is_correctPc` 的邏輯成立就行。

從 xor 的幾個 [小性質](https://en.wikipedia.org/wiki/Exclusive_or#Properties) 可以推得：如果 `a ^ b = c`，則 `a = c ^ b`（這邊就不證明了）。根據前面的性質，`a[i] ^ i == target[i]` 中的 `a[i]` 可以透過 `target[i] ^ i` 回推。



**IDA/Ghidra 解**

將 [task](release/task) 丟進 IDA/Ghidra decompile 後，可以看到幾乎是 source code 的程式了。

姑且不論整支程式到底寫了什麼，可以在 functions window 看到一個叫 `check_flag_is_correct()` 的 function。追進去後可以知道他其實就是檢查當 `i` 等於 0 到 25 時， `input[i] ^ i == target[i]` 是否都成立而已。

```cpp
i = 0LL;
isSame = 1;
do
{
  isSame = ((i ^ input[i]) == target[i]) & isSame;
  ++i;
}
while ( i != 25 );
return isSame;
```

根據 xor 的 [小性質](https://en.wikipedia.org/wiki/Exclusive_or#Properties) 可以推得：如果 `a ^ b = c`，則 `a = c ^ b`（這邊就不證明了）。根據前面的性質，`input[i] ^ i == target[i]` 中的 `input[i]` 可以透過 `target[i] ^ i` 回推。

