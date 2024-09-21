# Caption Styling Tool for Youtube
This tool serves the purpose of allowing formatting YouTube subtitles in `.ytt` (YouTube's internal formatting format), also known as `srt3`, through a simple format based on WebVTT. This format is not valid VTT, but it's easy to set up through a text editor.

This format should be labelled as `.vts3` (which stands for “`.vtt` to `.srt3`”). The program outputs two files: one for desktop and one for Android. This is due to YouTube's different handling of subtitles on different devices. It is advised to add a warning at the beginning of whichever is the default subtitle to switch to the appropriate version based on one's device. iOS is not currently supported due to lack of testing devices.

## Style definitions

In `srt3`, there are two types of definitions: window definitions and pen definitions.

Window definitions define the style of the subtitle window, including background color and text alignment. These apply to the entire caption.

Pen definitions define styles for text formatting, including text color and outline. These can apply either to the entire captions or to sections of it. Bold, italics, underlined and text size are also included in pen styles in `srt3`, but `vts3` handles them separately for convenience.

In `vts3`, definitions can be inserted anywhere: however, it is advised to put them at the beginning, after the fourth line of the file.

Spaces (U+‎0020 SPACE) are ignored when parsing a definition. A definition is made of the following elements:
* A character that specifies what is being defined. This character can be either `P` (‎‎U+0050 LATIN CAPITAL LETTER P) for pen definitions or `W` (U+‎0057 LATIN CAPITAL LETTER W) for window definitions.
* Two colons `:` (U+003A COLON)
* Either:
  * A comma-separated list of property-value pairs. Property names and their respective values must be separated by the character `:` (U+003A COLON). Property-value pairs must be separated by the character `,` (U+002C COMMA).
  * The string `DEF` (U+0044 LATIN CAPITAL LETTER D, U+‎0045 LATIN CAPITAL LETTER E, U+‎0046 LATIN CAPITAL LETTER F) followed by an integer. This is used to reference a style defined in the `default.vts3` file located in the same directory as the program. The integer determines which style is referenced: `1` references the first definition of that type (window or pen) in `default.vts3`, `2` references the second definition of that type, and so on.  

The following properties are allowed in window styles:
* `ah`: Determines the horizontal distance of the anchor point of the captions window from the left side of the captions area, as a percentage of the width of the captions area. Can be any unsigned (non-negative) integer or decimal (using `.` U+‎002E FULL STOP as the decimal separator). Values will be capped to 100 and decimals will be rounded to the nearest value.
  
  > Note: The captions area is a rectangle with the same center and shape as the video player (including the black bars at the sides), whose width and height are 96% of the player's width and height. This has two major consequences: first, that captions for 16:9 videos that use horizontal positioning far from the center of the video may not be compatible with cinema mode; secondly, that when using resolutions other than 16:9, the same issue may occur in fullscreen mode.
  > 
  > The behaviour of this property can change depending on the following settings defined in `settings.json`:
  > * `raw_positions`: Defaults to `true`. If set to `false`, values given will be interpreted as relative to the full player area, not just the captions area. Positions outside of the captions area will be clamped.
  > * `correct_positions`: Only used if `raw_positions` is set to `false`. Defaults to `"none"`. If set to `"fullscreen"`, the positions defined through `ah` and `av` will be interpreted as relative to the video area in fullscreen (excluding the black padding stripes), using the `aspect_ratio` setting to determine the video's aspect ratio. If set to `"optimize_pc"`, the positions will be changed to be as close as possible to the intended positions on both fullscreen and normal mode.
  
* `ap`: Determines the anchor point of the subtitle. Can take the following values:
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
  > Note: The subtitles area is a rectangle with the same center and shape as the video player (including the black bars at the sides), whose width and height are 96% of the player's width and height. This has two major consequences: first, that captions for 16:9 videos that use horizontal positioning far from the center of the video may not be compatible with cinema mode; secondly, that when using resolutions other than 16:9, the same issue may occur in fullscreen mode.
* `ju`: Determines text alignment. Can take the following values:
  * `0` or `left`: Aligns text to the left.
  * `1` or `right`: Aligns text to the right.
  * `2` or `center` : Aligns text to the center.
* 
