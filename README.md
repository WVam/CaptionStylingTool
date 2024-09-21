# Caption Styling Tool for Youtube
This tool serves the purpose of allowing formatting YouTube subtitles in `.ytt` (YouTube's internal formatting format), also known as `srt3`, through a simple format based on WebVTT. This format is not valid VTT, but it's easy to set up through a text editor.

This format should be labelled as `.vts3` (which stands for “`.vtt` to `.srt3`”). The program outputs two files: one for desktop and one for Android. This is due to YouTube's different handling of subtitles on different devices. It is advised to add a warning at the beginning of whichever is the default subtitle to switch to the appropriate version based on one's device. iOS is not currently supported due to lack of testing devices.

## Style definitions

In `srt3`, there are two types of definitions: window definitions and pen definitions.

Window definitions define the style of the subtitle window, including background color and text alignment. These apply to the entire caption.

Pen definitions define styles for text formatting, including text color and outline. These can apply either to the entire captions or to sections of it. Bold, italics, underlined and text size are also included in pen styles in `srt3`, but `vts3` handles them separately for convenience.
