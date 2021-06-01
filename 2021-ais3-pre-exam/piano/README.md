# [Reverse] Piano

- Points: 152
- Difficulty: ★
- Solves: 87/327 (Pre-exam), 2/190 (MyFirstCTF)
- Keywords: C#, .NET

## Descriptions

Is this a <span class="rainbow-text" style="font-family: Comic sans MS; font-size: 2rem; background-image: repeating-linear-gradient(45deg, violet, indigo, blue, green, yellow, orange, red, violet); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">MUSIC GAME</span>?

Author: CSY54

## Writeup

根據 `file` 的結果可以知道這題是 .NET reversing，而重要的檔案其實就 `piano.dll` 而已。

```shell
$ file piano.exe
piano.exe: PE32+ executable (GUI) x86-64, for MS Windows

$ file piano.dll
piano.dll: PE32 executable (GUI) Intel 80386 Mono/.Net assembly, for MS Windows
```

科普一下 .NET 的原理，整個概念其實跟 Java 及 JVM（Java Virtual Machine）差不多，有別於 C/C++ 編譯成原生 binary 的做法，Java 會將 source code 編譯成 bytecode，執行期間再透過 JVM 將 bytecode 轉成 machine code 執行；而 .NET 在 compile 階段會被編譯成 Common Intermediate Language（CIL），一樣是在執行期間才把它轉成 machine code 執行。這類語言通常相對 C/C++ 會比較好 reverse，因為在 compile 階段並不是編譯成原生的 binary，而是轉成一種中間的語言，這種中間語言能夠很好地被轉回 source code（差不多就相當於保留所有 symbol 並且沒有 optimize 過的 binary）。

至於 .NET reversing 的工具可以選擇 [dnSpy/dnSpy](https://github.com/dnSpy/dnSpy) 或 [icsharpcode/ILSpy](https://github.com/icsharpcode/ILSpy)。

將 `piano.dll` 拖進 dnSpy 後就可以看到 source code 了。以下是 decompile 出來的重點：

- `Piano()` 中定義了每個按鈕按下去後會呼叫 `onClickHandler()`
- `onClickHandler()` 中將按下的按鈕 index 丟進 `notes`，當 `notes` 的長度到達 14 後，會呼叫 `isValid()`；如果 `isValid()` 回傳 true，則顯示 `nya()` 回傳的資料
- `isValid()` 分別將第 `i` 項與第 `i + 1` 項的和與差去跟 `list` 及 `list2` 比較，如果都相同，則回傳 true；反之回傳 false

至於 `nya()` 的操作不重要，因為如果 `isValid()` 是成立的，它就會自動幫我們做 `nya()` 裡的操作並顯示回傳結果。

```c#
namespace piano {
  public class Piano : Form {
    public Piano() {
      this.buttons = new List<Button>{ this.C, this.D, this.E, this.F, this.G, this.A, this.B, this.CSharp, this.DSharp, this.FSharp, this.GSharp, this.ASharp };
      foreach (Button button in this.buttons) {
        button.Click += this.onClickHandler;
      }
    }

    private void onClickHandler(object sender, EventArgs e) {
      Button button = (Button)sender;
      this.notes.Add(this.buttons.IndexOf(button));
      if (this.notes.Count == 14) {
        if (this.isValid()) {
          MessageBox.Show(this.nya());
        }
        this.notes.RemoveAt(0);
      }
    }

    private bool isValid() {
      List<int> list = new List<int>{ 14, 17, 20, 21, 22, 21, 19, 18, 12, 6, 11, 16, 15, 14 };
      List<int> list2 = new List<int>{ 0, -3, 0, -1, 0, 1, 1, 0, 6, 0, -5, 0, 1, 0 };
      for (int i = 0; i < 14; i++) {
        if (this.notes[i] + this.notes[(i + 1) % 14] != list[i]) {
          return false;
        }
        if (this.notes[i] - this.notes[(i + 1) % 14] != list2[i]) {
          return false;
        }
      }
      return true;
    }

    private string nya() {
      List<int> list = new List<int>{ 70, 78, 89, 57, 112, 60, 125, 96, 103, 104, 50, 109, 87, 115, 112, 54, 100, 97, 103, 56, 85, 101, 56, 119, 119, 100, 59, 88, 50, 48, 62, 120, 84, 58, 100, 86, 74, 92, 54, 96, 60, 117, 119, 122 };
      List<char> list2 = new List<char>();
      for (int i = 0; i < list.Count; i++) {
        list2.Add((char)(list[i] ^ this.notes[i % this.notes.Count]));
      }
      return new string(list2.ToArray());
    }
  }
}
```

也就是說，只要找到能讓 `notes` 內的數字符合和與差跟 `isValid()` 中的 `list` 及 `list2` 相同即可，並根據 `buttons` 中定義的順序按下就可以拿到 flag 了。

