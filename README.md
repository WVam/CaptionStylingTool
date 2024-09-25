# Caption Styling Tool for Youtube
This tool serves the purpose of allowing formatting YouTube subtitles in `.ytt` (YouTube's internal formatting format), also known as `srt3`, through a simple format based on WebVTT. This format is not valid VTT, but it's easy to set up through a text editor.

This format should be labelled as `.vts3` (which stands for “`.vtt` to `.srt3`”). The program outputs two files: one for desktop and one for Android. This is due to YouTube's different handling of subtitles on different devices. It is advised to add a warning at the beginning of whichever is the default subtitle to switch to the appropriate version based on one's device. iOS is not currently supported due to lack of testing devices.

## Sample document

```
WEBVTT

P1 :: fc: cyan
P2 :: fs: cursive
W1 :: ap: 3, av: 50, ah: 0
W2 :: ap: 5, av: 50, ah: 100

00:11.000 --> 00:13.000
We are in * New York City *

00:13.000 --> 00:16.000
We’re actually at the * Lucern Hotel !* , just down the street

00:16.000 --> 00:18.000
from the % American Museum of Natural History %

00:18.000 --> 00:20.000
And with me is @150 Neil deGrasse Tyson

NOTE This is a good place to mention that, while most VTT features don't work, comments do.

00:20.000 --> 00:22.000
Astrophysicist, Director of the Hayden Planetarium

00:22.000 --> 00:24.000
at the AMNH.

00:24.000 --> 00:26.000
Thank you for walking down here.

00:27.000 --> 00:30.000
And I want to do a $1._ follow-up _ on $ the last conversation we did.

00:30.000 --> 00:31.500
When we e-mailed—

00:30.500 --> 00:32.500
#1.€1.@75 Didn’t we talk about enough in that conversation?

00:32.000 --> 00:35.500
#2.@75 No! No no no no; 'cos 'cos obviously 'cos

00:32.500 --> 00:33.500
#1.€1.@75._ Laughs

00:35.500 --> 00:38.000
You know I’m so excited my €2@200 glasses & are falling off here.
```

## Style definitions

In `srt3`, there are three types of definitions: window style definitions, window position definitions and pen definitions.

Window style definitions define text alignment and orientation. These apply to the entire caption.

Window position definitions define the position and anchor point of the caption. These apply to the entire caption.

Pen definitions define styles for text formatting, including text color and outline. These can apply either to the entire captions or to sections of it. Bold, italics, underlined and text size are also included in pen styles in `srt3`, but `vts3` handles them separately for convenience.

In `vts3`, there are only two types of definitions: window position definitions (window definitions for short) and pen definitions. Since there are only 15 valid window styles definitions, they will all be automatically added to the final `srt3` file. Definitions can be inserted anywhere after the header lines: however, they must be placed before the first time they are referenced, and it is advised to put them at the beginning, immediately before the first cue.

Spaces (U+‎0020 SPACE) are ignored when parsing a definition. A definition is composed of the following elements:
* A character that specifies what is being defined. This character can be either `P` (‎‎U+0050 LATIN CAPITAL LETTER P) for pen definitions or `W` (U+‎0057 LATIN CAPITAL LETTER W) for window definitions.
* A string of characters that does not contain two consecutive colons `:` (U+003A COLON). This is not parsed, but it can be useful in order to annotate the ordinal position of each definition.
* Two colons `:` (U+003A COLON).
* Either:
  * A comma-separated list of property-value pairs. Property names and their respective values must be separated by the character `:` (U+003A COLON). Property-value pairs must be separated by the character `,` (U+002C COMMA).
  * The string `DEF` (U+0044 LATIN CAPITAL LETTER D, U+‎0045 LATIN CAPITAL LETTER E, U+‎0046 LATIN CAPITAL LETTER F) followed by an integer. This is used to reference a style defined in the `default.vts3` file located in the same directory as the program. The integer determines which style is referenced: `1` references the first definition of that type (window or pen) in `default.vts3`, `2` references the second definition of that type, and so on.  

The following are valid definitions:
```
W1 :: ah: 40, av: 20, ap: 3
W 34 ::ah:   34,av:99, a    p   : 2
W :: ah: 30, av: 45
P::fc:#ffff00
P abcdefghijk:lmn:as :: fc : # 0 0 0 0 f f
P 987 6543 :: DE F2
```

However, for ease of use and of reading, it is advised to write them in one of the following three styles:
```
W 1 :: ah: 40, av: 20, ap: 3
W 2 :: ah: 34, av: 99, ap: 2
W 3 :: ah: 30, av: 45
P 1 :: fc: #ffff00
P 2 :: fc: #0000ff
P 3 :: DEF 2
```
```
W1 :: ah: 40, av: 20, ap: 3
W2 :: ah: 34, av: 99, ap: 2
W3 :: ah: 30, av: 45
P1 :: fc: #ffff00
P2 :: fc: #0000ff
P3 :: DEF2
```
```
W :: ah: 40, av: 20, ap: 3
W :: ah: 34, av: 99, ap: 2
W :: ah: 30, av: 45
P :: fc: #ffff00
P :: fc: #0000ff
P :: DEF 2
```
```
W :: ah: 40, av: 20, ap: 3
W :: ah: 34, av: 99, ap: 2
W :: ah: 30, av: 45
P :: fc: #ffff00
P :: fc: #0000ff
P :: DEF2
```

### Window definitions

* `ah`: Determines the horizontal distance of the anchor point of the captions window from the left side of the captions area, as a percentage of the width of the captions area. Can be any unsigned (non-negative) integer or decimal (using `.` U+‎002E FULL STOP as the decimal separator). Values will be capped to 100 and decimals will be rounded to the nearest value.
  
  > Note: The captions area is a rectangle with the same center and shape as the video player (including the black bars at the sides), whose width and height are 96% of the player's width and height. This has two major consequences: first, that captions for 16:9 videos that use horizontal positioning far from the center of the video may not be compatible with cinema mode; secondly, that when using resolutions other than 16:9, the same issue may occur in fullscreen mode.
  > 
  > The behaviour of this property can change depending on the following settings defined in `config.json`:
  > * `raw_positions`: Defaults to `true`. If set to `false`, values given will be interpreted as relative to the full player area, not just the captions area (so, for example, `25` will correspond to a quarter of the entire player area, whereas with `raw_positions` set to `false` the correct number would be `24`). Positions outside of the captions area will be clamped.
  > * `correct_positions`: Only used if `raw_positions` is set to `false`. Defaults to `"none"`. If set to `"fullscreen"`, the positions defined through `ah` and `av` will be interpreted as relative to the video area in fullscreen (excluding the black padding stripes), using the `aspect_ratio` setting to determine the video's aspect ratio. If set to `"optimize"`, the positions will be changed to be as close as possible to the intended positions on both fullscreen and normal mode.
  
* `ap`: Determines the anchor point of the subtitle. Can be any of the following values:
  * `0`: Top left.
  * `1`: Top center.
  * `2`: Top right.
  * `3`: Center left.
  * `4`: Center.
  * `5`: Center right.
  * `6`: Bottom left.
  * `7`: Bottom center.
  * `8`: Bottom right.
  
  >  Note: A caption with an anchor at the top can be pushed by the top of the player. A caption with an anchor at the bottom can be pushed by the bottom of the player.
 
* `ah`: Determines the vertical distance of the anchor point of the captions window from the top side of the captions area, as a percentage of the height of the captions area. Can be any unsigned (non-negative) integer or decimal (using `.` U+‎002E FULL STOP as the decimal separator). Values will be capped to 100 and decimals will be rounded to the nearest value.
  
  > Note: The captions area is a rectangle with the same center and shape as the video player (including the black bars at the sides), whose width and height are 96% of the player's width and height. This means that, for videos using wide aspect ratios, vertical positioning may be different than the expected positioning in cinema and fullscreen mode.
  > 
  > The behaviour of this property can change depending on the following settings defined in `config.json`:
  > * `raw_positions`: Defaults to `true`. If set to `false`, values given will be interpreted as relative to the full player area, not just the captions area (so, for example, `25` will correspond to a quarter of the entire player area, whereas with `raw_positions` set to `false` the correct number would be `24`). Positions outside of the captions area will be set to the nearest position inside the captions area. Values will be rounded to the nearest integer after being converted to the correct value used by `srt3`.
  > * `correct_positions`: Only used if `raw_positions` is set to `false`. Defaults to `"none"`. If set to `"fullscreen"`, the positions defined through `ah` and `av` will be interpreted as relative to the video area in fullscreen (excluding the black padding stripes), using the `aspect_ratio` setting to determine the video's aspect ratio. If set to `"optimize"`, the positions will be changed to be as close as possible to the intended positions on both fullscreen and normal mode.

### Pen definitions

The following properties are allowed in pen definitions:
* `bc`: Determines the color of the caption background. Can be any color code (`#` U+‎0023 NUMBER SIGN followed by 6 hexadecimal digits) other than `#000000` and `#ffffff` or one of the supported [color names](#color-names).
* `bo`: Determines the opacity of the background. Can be a number from `0` (completely transparent) to `254` (practically completely opaque).
* `ec`: Determines the color of the text edge. Can be any color code (`#` U+‎0023 NUMBER SIGN followed by 6 hexadecimal digits) other than `#000000` and `#ffffff` or one of the supported [color names](#color-names).
* `et`: Determines the style of the text edge. Can be any of the following values:
  * `1` or `solid-shadow`: Hard shadow.
  * `2` or `solid`: Outline-like effect (double shadow).
  * `3` or `glow`: Blurred outline.
  * `4` or `soft-shadow`: Soft shadow.
  > This is how the outlines look like:
  > 
  > ![Screenshot with different outlines](https://github.com/user-attachments/assets/2cdf9067-fc9a-42c7-b7c2-7898241b29df)
* `fc`: Determines the color of the text. Can be any color code (`#` U+‎0023 NUMBER SIGN followed by 6 hexadecimal digits) other than `#000000` and `#ffffff` or one of the supported [color names](#color-names).
* `fo`: Determines the opacity of the text. Can be a number from `0` (completely transparent) to `254` (practically completely opaque).
* `fs`: Determines the font of the text. Can be any of the following values:
  * `1` or `monospace-serif`: Monospace Serif (Courier New).
  * `2` or `serif`: Serif (Times New Roman).
  * `3` or `monospace-sans-serif`: Monospace Sans-Serif (Lucida Console).
  * `4` or `sans-serif`: Sans-Serif (default, Roboto).
  * `5` or `fantasy`: Fantasy/Casual (Comic Sans).
  * `6` or `cursive`: Cursive/Script (Comic Sans).
  * `7` or `small-caps`: Small Caps (Arial).

### Color names

The following color names are supported:
* `black`: Equal to `#080808` (default background color).
* `white`: Equal to `#fefefe`.
* `gray` or `grey`: Equal to `808080`.
* `red`: Equal to `#ff0000`.
* `yellow`: Equal to `#ffff00`.
* `lime`: Equal to `#00ff00`.
* `cyan`: Equal to `#00ffff`.
* `blue`: Equal to `#0000ff`.
* `magenta`: Equal to `#ff00ff`
* `maroon`: Equal to `#800000`.
* `olive`: Equal to `#808000`.
* `green`: Equal to `#008000`.
* `teal`: Equal to `#008080`.
* `navy`: Equal to `#000080`.
* `purple`: Equal to `#800080`.
* `pink`: Equal to `#ffc0cb`.
* `orange`: Equal to `#ffa500`.
* `gold`: Equal to `#ffd700`.
* `orangered`: Equal to `#ff4500`.
* `goldenrod`: Equal to `#daa520`.

## Words

A caption is made of lines, separated from each other by a single newline (000A LINE FEED (LF)). Each line is made of words. Words are strings of characters that don't contain spaces (U+‎0020 SPACE), separated from each other by a single space (U+‎0020 SPACE). For example, the line:
```
Menin aeide th€4  pel314 d€W AXILHOS
```
is composed of the words `"Menin"`, `"aeide"`, `"th€a"`, `""` (an empty string), `"pel314"`, `"d€W"` and `"AXILHOS"`.

Some words have special functions. There special words are divided into five categories: escapes, style codes, time codes, offset text and ruby text.

### Escapes

Escapes are all words longer than 1 character which begin with the character `:` (U+003A COLON). These words will be rendered as they are written, without the first character (i.e., the colon). This is useful for displaying sequences of character that would otherwise be interpreted as special words (e.g. `$200`).

### Style codes

Style codes are special words that change the styling of text. They are divided into two categories:
* **Style setters**: Style codes that begin with the character `#`. These set the default style for the entire window.
* **Style switches**: All other style codes. These style codes are used to change the style of part of a caption.

A style code is composed of the following elements:
* One of the following:
  * Nothing.
  * The character `!` (U+0021 EXCLAMATION MARK). If the style code starts with an exclamation mark, then the previous and following word will be joined together in the final subtitle instead of being separated by a space. For example, `It's _ me !_ , Joe!` will be rendered as "It's *me*, Joe!" rather than "It's *me* , Joe!".
  * A window setter. The window setter marks everything that follows as part of a new window. It also marks the style code as a style setter. A window setter is composed of the following elements:
    * The character `#` (U+‎0023 NUMBER SIGN).
    * (Optional) An unsigned (positive) integer. This integer indicates the window position to use. if a number N is specified, then the Nth window definition inside the `.vts3` file will be used. For example, if the code begins with `#1`, the new window will use the window position defined in the first window definition of the file. If an integer is not specified, then YouTube's default window style will be used.
    * (Optional) A two-character string to determine text alignment inside the new window.
      * The first character must be one of the following:
        * `l` (U+‎006C LATIN SMALL LETTER L): Left-aligned text.
        * `r` (U+0072 LATIN SMALL LETTER R): Right-aligned text.
        * `c` (U+0063 LATIN SMALL LETTER C): Center-aligned text (default).
      * The second character must be one of the following:
        * `h` (U+0068 LATIN SMALL LETTER H): Horizontal text (default).
        * `u` (U+0075 LATIN SMALL LETTER U): Upright text (vertical text, does not rotate letters), columns right-to-left.
        * `U` (U+0055 LATIN CAPITAL LETTER U): Upright text, columns left-to-right.
        * `s` (U+0073 LATIN SMALL LETTER S): Sideways text (text rotated by 90° counterclockwise), columns left-to-right.
        * `S` (U+0053 LATIN CAPITAL LETTER S): Sideways text, columns right-to-left.
* Any combination of the following characters or character sequences, called **switches**:
  * The *italics* switch `_` (U+005F LOW LINE). This switch enables or (if it was already enables) disables italics style for the following words.
  * The **bold** switch `*` (U+‎002A ASTERISK). This switch enables or (if it was already enables) disables bold style for the following words.
  * The <ins>underline</ins> switch `%` (U+‎‎0025 PERCENT SIGN). This switch enables or (if it was already enables) disables underlined style for the following words.
  * A pen switch. This switch changes the pen style for the following words. A pen switch is composed of the following elements:
    * Either the character `€` (U+20AC EURO SIGN) or the character `$` (U+‎0024 DOLLAR SIGN). The two characters are interchangeable.
    * (Optional) An unsigned (positive) integer. This integer indicates the pen to use for the following words. if a number N is specified, then the Nth pen definition inside the `.vts3` file will be used. For example, if the code begins with `#1`, the following words will use the pen style defined in the first pen definition of the file. If an integer is not specified, the behaviour will change depending on whether the switch is part of a style switch or a style setter.
      * If the pen switch is part of a style switch, then the following words will use the window's default pen. That is the pen referenced by the style switch inside the window's style setter or, in absence of that, YouTube's default style.
      * If the pen switch is part of a style setter, then YouTube's default pen style will become the window's default pen style. Note that this is the case even if no pen switch is added to the style setter: therefore, it is recommended *not* to add value-less pen switches inside style setters.
    * (Optional) Either of the following characters:
      * `+` (U+‎002B PLUS SIGN): The pen switch only overrides the previous pen style's text attributes (everything except `bc` and `bo`).
      * `-` (U+002D HYPHEN-MINUS): The pen switch only overrides the previous pen style's background attributes (`bc` and `bo`).
  * A size switch. This switch changes the size of the following words. A size switch is composed of the following elements:
    * The character `@` (U+0040 COMMERCIAL AT).
    * An unsigned (non-negative) integer greater or equal to 300. This integer indicates the size to use for the following words. It indicates the size relative to YouTube's default size in four-hundredths (1/400s). Therefore, in order to make text twice as big as normal, you will need to use the number 800.
  * The reset switch `&` (U+‎0026 AMPERSAND). It resets everything to the style indicated in the window's style setter (or, in absence of that, to YouTube's default style). This applies before all other switches.
  > Note: The difference between the reset switch `&` and a value-less pen switch `€`/`$` is that the latter only resets the style attributes that are specified in a pen definition (like font color, font family, outlines, etc.), while `&` resets everything (including size, italics, bold, etc.)

A few things to note:
- Dots `.` (U+‎002E FULL STOP) are removed from style codes when they are parsed. This means that you can use dots in order to separate the elements of style codes for your own convenience.
- A switch at the end of the caption will be discarded. If a switch is added at the end of a line, no additional space will be added between the last word and the newline.
- The combination of switches at the end of a style code can be composed of no switches. This means that empty strings will be considered style switches and removed upon parsing. This also means that multiple spaces will not be counted. If you want your space to count, please use `&#160;` (which results in U+‎00A0 NO-BREAK SPACE).
- It is recomended to "close" italics, bold and underline switches, as if they were Markdown elements, for the sake of clarity.

### Time codes

Time codes serve the purpose of making the following words appear at a later time (like karaoke).

There are two kinds of time code: relative and absolute. Relative time codes start with a single `;` (U+‎003B SEMICOLON) and they indicate how much time after the beginning of the line the following words should be shown. Absolute time codes start with a double semicolon `;;` and indicate the absolute time at which the following words should be displayed.

A time code is composed of the following elements:
* The character `;` (U+‎003B SEMICOLON).
* (Optionally) One digit to indicate how many minutes after the beginning of the caption the following words should play, followed by the character `:` (U+003A COLON).
* Two digits to indicate how many seconds after the beginning of the caption the following words should play. These are added to the minutes specified previously.
* The `.` (U+‎002E FULL STOP) character.
* Three digits to indicate how many milliseconds afrer the beginning of the caption the following words should play. These are added to the minutes and seconds specified previously.

An absolute time code is composed of the following elements:
* The string `;;` (U+‎003B SEMICOLON, U+‎003B SEMICOLON).
* A [WebVTT timestamp](https://www.w3.org/TR/webvtt1/#webvtt-cue-timings) indicating the absolute time in the video at which the following words should be displayed.

### Offset text

Offset text are all words that start and end with the character `^` (U+002A ASTERISK) or start and end with the character `_` (U+005F LOW LINE). It is used to display subscript or superscript text.

Offset text is composed of the following elements:
* The opening character. It can be any of the following:
  * `*` (U+002A ASTERISK): It indicates that the text between the closing and opening carets must be superscript.
  * `_` (U+005F LOW LINE): It indicates that the text between the closing and opening carets must be subscript.
* (Optionally) The escape character `:`. It prevents the following characters from being parsed as a spacing controller (see below). The colon will be removed from the offset text.
* (Optionally) A spacing controller, which determines how that text is spaced from surrounding words. A spacing controller is composed of the following elements:
  * The character `!` (U+0021 EXCLAMATION MARK).
  * A two-character string which can be any of the following:
    * `00` (U+0030 DIGIT ZERO, U+0030 DIGIT ZERO): Joined with the words on both sides.
    * `01` (U+0030 DIGIT ZERO, U+0031 DIGIT ONE): Joined with the word on the left (default behavior).
    * `10` (U+0031 DIGIT ONE, U+0030 DIGIT ZERO): Joined with the word on the right.
    * `11` (U+0031 DIGIT ONE, U+0031 DIGIT ONE): Joined with neither word.
* The text to display as superscript or subscript.
* The closing character. It must be the same as the opening character.

### Ruby text

Ruby text is used to display furigana and similar annotations for CJK.

