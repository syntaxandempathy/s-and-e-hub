I’ve been thinking about how I’m using little tools like browser extensions in Chrome, which thankfully work well, and I thought it might be useful to write some small bits and pieces about how that works.

My first one, which I’ve been using a lot, is the FireShot extension for screenshots. It allows you to do a full screen, auto-scroll, or select regions—even ones with JavaScript-filled elements. What I’ve been doing with that is capturing outputs from things I’ve worked on with AI, or screenshots of something I saw someplace else, even if unrelated—basically anything that’s an image.

I’ve started using FireShot when I have a desired output. If it’s an image, I can show it to the AI and take advantage of multimodal features. For example, in a Colab notebook with three different sessions going—ChatGPT playing individual roles and mimicking agents—I can take a screenshot of a conversation, the notebook, and the outputs (a lot of which have visualizations). Then I can get feedback from the “expert,” the “visualization reviewer,” and the “code reviewer.” Instead of assuming the AI will figure out what would happen from just the code, I can show it what actually happened.

This doesn’t have to be limited to FireShot. The built-in screenshot tool in iOS, or desktop screenshot tools, also work. They can capture the full desktop, a window, or a region, which reduces the chance of including unnecessary clutter that might confuse the AI.

Today, for example, I found out one of the actions I have running in GitHub wasn’t sending what I wanted—it was just summarizing. I took a screenshot, popped it into a GitHub issue, and asked Claude to look into it and provide a plan to fix it. I haven’t verified the plan yet, but I know it’s going to work.

The point is that communicating with LLMs isn’t limited to text. You can put in an image and ask it to read, summarize, or generate text from it. More importantly, this can be built into workflows and processes.

I haven’t done this yet, but the next step would be automating it: set up an action that runs and outputs both visual and non-visual results, saves them as an image or a PDF, and then feeds that into another action. That action could process everything and add a results page to the PDF. In the morning, I’d review the output. If I want to validate it, I’d have all the inputs in the PDF as well.

That’s probably more than one article, but there you go.