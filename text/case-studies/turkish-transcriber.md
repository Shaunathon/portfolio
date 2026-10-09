# Case study page: shaunburley.com/work/turkish-transcriber/
# Lines at the top that start with a capital letter (Role, Built with, Try it) make the facts box under the title.
# Images: ![description for screen readers](file name){.wide} on one line, the caption on the line right under it.
#   Sizes: .wide (full width), .tall (narrow and tall), .small (shown at its own size); add .scroll for images too wide for phones.
# Each ### heading starts a key decision box; a paragraph starting with **Tradeoff:** gets the shaded style.
# A line made only of links with {.button} after them becomes a row of buttons.

tab title: Turkish voice and video transcriber · Shaun Burley
description: An AI study tool I designed and built that turns Turkish audio into side-by-side Turkish and English study pages.
short title: Turkish transcriber
eyebrow: Case study · Personal project
title: A study tool that shows its work: Turkish voice and video transcriber
Role: Designer and builder, with Claude writing most of the code
Built with: Whisper for transcription, GPT for translation, Python, GitHub Pages
Try it: [Live transcripts site](https://shaunathon.github.io/youtube-turkish-transcriber/) · [Code on GitHub](https://github.com/Shaunathon/turkish-voice-transcriber)
next title: One design system for a growing product suite
next link: work/design-system/
---
## Summary

Turkish arrives faster than I can follow it. Fellow students further along than me send voice messages every week, and I have a backlog of Turkish music lessons on YouTube. YouTube's auto-transcribe gets too much wrong to learn from, and it has no idea it's listening to a music lesson.

So I designed and built a tool that transcribes Turkish audio, translates it sentence by sentence, and turns it into a study page with Turkish and English side by side. Videos get a transcript that follows along with playback. Voice messages get vocabulary and grammar notes, so each message becomes a lesson.

![A transcript page for a Turkish clarinet lesson video. A list of lessons runs down the left. The embedded YouTube video sits above an 'Autoscroll: active' label, and below it the transcript appears in two columns, Turkish on the left and English on the right, with the current sentence highlighted.](transcriber-video.webp){.wide}
A lesson page: the video, an "Autoscroll: active" label that explains why the page is moving, and the transcript in two columns.

## My role

I own the problem, the decisions and the judgment; Claude wrote most of the code. I tested each version on a real lesson or message, logged everything that was wrong, and handed Claude the whole list of fixes at once. Then I checked the result against the audio again.

## Key decisions

### 1. Keep the source next to the translation.

Every page shows Turkish and English side by side, never English alone. Consistent spacing keeps each Turkish sentence level with its English pair, so the two never drift apart down the page.

**Tradeoff:** English alone would read faster. But it would hide the AI's mistakes and stop me learning the language. Side by side, I can check every line of the translation against the original.

### 2. Translate whole sentences, not fragments.

My first version translated each timestamped fragment from the transcription on its own. Both columns came out choppy, and the translation lost meaning. I switched to grouping fragments into whole sentences first, then translating each sentence. Each pair keeps the timestamp where it starts, so clicking a line still jumps the video there. The Turkish is rebuilt from the original fragments, so the AI never rewords the source.

**Tradeoff:** more processing logic to maintain. In return, the source stays exactly as spoken and the translation makes sense.

### 3. Tell the AI what it's listening to.

Both the transcription and the translation are told the audio is a music lesson, so they expect music terms instead of guessing. The catch that led here: <i lang="tr">çarpma</i>, a kind of ornament, kept coming out as "hit" or "strike" until I added music terminology to the translation prompt.

**Tradeoff:** a built-in assumption helps on lessons and hurts on everything else. That's the first thing I'd change.

## What shipped

- A public site of transcribed Turkish music lessons, where you can click any line to jump the video there and let the transcript scroll along.
- Voice message pages with an audio player, playback speeds from 0.5x to 1.25x, a vocabulary table and grammar notes.
- Open-source code that accepts common audio formats, so anyone can transcribe their own files.

![The lower half of a voice message page: a vocabulary table listing Turkish words, their English meanings and short notes, followed by four grammar notes that explain constructions used in the message.](transcriber-voice-notes.webp)
Under each voice message: the words and grammar worth learning from it.

[Try the live transcripts](https://shaunathon.github.io/youtube-turkish-transcriber/){.button .primary} [See the code](https://github.com/Shaunathon/turkish-voice-transcriber){.button}

## Evidence

I built it for my own study and I'm its main user so far. What it showed me:

- **Context is what makes AI transcription and translation accurate.** Most of my audio is music lessons, and both passes do far better when they assume a musical context.
- **A layout decision taught me something about the language.** Once each sentence pair lined up, the extra space on either side showed which kinds of expressions Turkish says more compactly than English, and the other way round.
- **Showing the source is how the tool earns trust.** It's the same principle as my assistant work at UiPath: the AI's output never hides what it came from, so the person can check it.

## What I'd change

Instead of always assuming a music lesson, I'd have the tool ask what context to assume before it transcribes anything. It follows straight from the main thing I learned: context drives accuracy, so the person who knows the context should be able to supply it.
