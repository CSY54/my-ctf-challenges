# 2021 AIS3 Pre-exam / MyFirstCTF

在這場比賽中我一共出了三道 reverse 的題目，恰好 Pre-exam 一題、MyFirstCTF 一題、Pre-exam + MyFirstCTF 一題。對於這場 CTF 我的出題方向是想要多元一點，也因此我出了一題簡單的 ELF、一題簡單的 .NET、以及一題 Arduino 的逆向，巧的是這場 reverse 類別的題目領域恰好都沒有交集，除了我的三題外，還有一題混淆後的 JavaScript 逆向、一題 Pickle bytecode 的逆向、一題相對複雜的 ELF（我的 ELF 題是 MyFirstCTF only，而這題是 Pre-exam only），恰好跟我當初的想法一致。

對於 MyFirstCTF only 的 ⒸⓄⓋⒾⒹ-①⑨ 是除了 pwn 以外各類別的第一題中最少人解的題目有點意外，原先預期的難度應該要是再多一點人解，不知道是不是因為用了 ncurses 的原因，讓整段 code 變得沒有那麼單純，導致可能有新手打開就放棄了。

至於 Pre-exam 跟 MyFirstCTF 都有的 Piano，作為簡單的 .NET 逆向，在 Pre-exam 的解題人數大致符合我的預期，不過在 MyFirstCTF 預期是要再多一點人解的。然而根據賽後的回饋表單，好像有部分的人在看到是 exe 檔就放棄了...

最後是 Pre-exam only 的 The Secret Lock，最初在出題時就被其他出題者說可能會是魔王題的存在了。就出題的觀點來看，這題的考點大概就跟逆向一般的 binary 差不多，只不過 ISA 是 AVR 就是了。在出題的時候，我有刻意用別人包好的 library，讓整份 code 能夠從比較高階的方式去操控其他元件，而非去做一堆繁複的訊號操作，也就出現了提示所說的「The buttons are configured to use the ASCII value of the character written on the picture.」另外，這題在編譯的時候開了 `-O0` 且 source code 也有刻意寫成類似 loop unroll 的結構，從解題的角度來看，看到這段程式碼基本上這題就做完了，然而從賽後的回饋表單看起來好像沒人碰到這段過... 最後我想要說聲抱歉，對於在第一個提示釋出前沒有透露任何有關圖中的板子是 Arduino Uno 這點是我的失誤，原本應該在題目中提到的才對，不過後來忘記放上去了，抱歉。

總之，這場比賽是一次愉快的經驗，作為出題者的我也學了 ncurses、C# 這些平常可能沒機會碰到的東西，同時在題目的設計上也相較之前多了一點想法，最後希望參加的參賽者也能夠從我的題目中學到東西。
