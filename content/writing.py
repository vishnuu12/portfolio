"""
Three notes.

Written from work that actually exists - the code is public and the numbers are
the numbers the tests print. They are short on purpose: a note that takes ten
minutes to read is a note nobody reads.

Block types the generator understands:
    {"p": "..."}      a paragraph
    {"h": "..."}      a sub-heading
    {"list": [...]}   a bullet list
    {"code": "..."}   a code block
    {"quote": "..."}  a pull quote
"""

NOTES = [
    {
        "slug": "gradient-descent-twice",
        "title": "Writing gradient descent from scratch, twice",
        "date": "October 2026",
        "reading": "6 min",
        "summary": (
            "I built fifteen machine-learning concepts from scratch in NumPy, then "
            "ported the maths to JavaScript so the site could have sliders. Two "
            "implementations of the same algorithm is a liability - unless something "
            "keeps them honest."
        ),
        "tags": ["Python", "NumPy", "JavaScript", "Testing"],
        "body": [
            {
                "p": "The first version was easy to justify. I could have called "
                "scikit-learn in three lines, but then I would still not know what it "
                "was doing. So linear regression, logistic regression, k-means, PCA "
                "and a small neural network all got written out by hand, with the "
                "gradient spelled out next to the loss."
            },
            {
                "p": "The second version was not planned. Once the demos existed as "
                "Python scripts, the obvious next thing was a page where you could "
                "drag the learning rate and watch the loss curve change. The browser "
                "cannot run NumPy, so the maths had to be written again in JavaScript."
            },
            {"h": "Two implementations, one truth"},
            {
                "p": "Now I had the same algorithm in two languages, which is a "
                "well-known way to end up with two different algorithms. The fix was "
                "to make the tests assert the same properties on both sides - not "
                "that the code runs, but that it is right:"
            },
            {
                "list": [
                    "gradient descent on a single parameter lands on the mean of the data",
                    "linear regression recovers a slope of 2 from noisy points",
                    "a learning rate of 1.0 diverges while 0.05 converges",
                    "degree-15 polynomial: training error falls, test error climbs, ridge pulls it back",
                    "k-means recovers centres it was never shown",
                    "the top two principal components carry more than 90% of the variance",
                    "a hidden layer beats a linear model on a ring the line cannot split",
                ]
            },
            {
                "p": "Both suites run in CI, the JavaScript one under Node inside "
                "pytest. If the Python moves, the JavaScript has to move with it or "
                "the build fails."
            },
            {"h": "What it caught"},
            {
                "p": "Two things I would not have found otherwise."
            },
            {
                "p": "The first was a real bug in a tool that evaluates arithmetic. "
                "It stripped whitespace before parsing, which is fine until the model "
                "hands it something like 5 apples plus 3 oranges. After stripping, "
                "the digits sit next to each other and it parses as 53 - a confident, "
                "wrong answer, produced by the exact function written to prevent "
                "confident, wrong answers."
            },
            {
                "code": "\"5   3\"   ->  53      # strip whitespace, then parse\n\"5   3\"   ->  error   # skip whitespace between tokens"
            },
            {
                "p": "The second was quieter. Retrieval was only finding the right "
                "document 5 times out of 6, and the reason was that every question "
                "and every document contains the same words - the, is, of, what. "
                "Matching on those is close to matching at random. Dropping short "
                "words and stopwords before hashing took it to 6 out of 6."
            },
            {
                "quote": "The cheapest improvement to a keyword retriever is to stop "
                "matching on the words that are in everything."
            },
            {
                "p": "None of this is exotic. It is just the ordinary discipline of "
                "writing down what must be true, and then making the machine check "
                "it every time you change something."
            },
        ],
    },
    {
        "slug": "prompts-are-code",
        "title": "Prompts are code",
        "date": "October 2026",
        "reading": "5 min",
        "summary": (
            "A prompt has parts with different jobs, and the output contract is not "
            "optional. How I structure prompts so they survive contact with real "
            "input - and why the repair loop has to know when to give up."
        ),
        "tags": ["LLM", "Prompt engineering", "RAG"],
        "body": [
            {
                "p": "Most of the prompt engineering I do at work is not about finding "
                "magic words. It is about structure: putting each thing in the place "
                "where it does its job, and treating the output like an interface "
                "rather than a sentence."
            },
            {"h": "The parts"},
            {
                "list": [
                    "system - who the model is, the rules it must follow, and the output contract",
                    "user - the request and the data it needs, clearly fenced as data",
                    "assistant - one or two examples of exactly the answer you want",
                    "tool - results of the tools the model asked you to run",
                ]
            },
            {
                "p": "The system message is the part people under-use. If you want "
                "JSON, say so there, name the keys, and say what to do when a value "
                "is missing. That single paragraph removes most of the formatting "
                "drift you would otherwise chase with retries."
            },
            {"h": "Fence the data"},
            {
                "p": "Retrieved documents and user input are untrusted. Put them in a "
                "labelled block and tell the model to answer from that block and cite "
                "which part it used. Numbering the passages does two things at once: "
                "it gives the model something to cite, and it gives you something to "
                "check the answer against."
            },
            {"h": "Validate, then repair, then give up"},
            {
                "p": "The step people skip is validation. A successful JSON parse is "
                "not a valid object - it can be missing fields, or hold nulls where "
                "you needed strings, and that failure surfaces much later as a "
                "KeyError somewhere far from the cause."
            },
            {
                "code": "for attempt in range(1, max_attempts + 1):\n"
                "    response = llm.chat(messages)\n"
                "    payload  = try_parse_json(response.text)     # may be None\n"
                "    problems = validate(payload)                 # your schema\n"
                "    if not problems:\n"
                "        return payload\n"
                "    messages += [assistant(response.text), user(f'rejected: {problems}')]\n"
                "return None      # give up and tell the user"
            },
            {
                "p": "The last line is the important one. Some failures cannot be "
                "repaired: if the input genuinely does not contain the email address "
                "you asked for, no number of retries invents it. Past two or three "
                "attempts you are spending money to hide a problem the user should "
                "be told about. I have watched a loop run five times on an impossible "
                "request and report success."
            },
            {"h": "Two costs that are easy to forget"},
            {
                "p": "Few-shot examples are worth it when the format is easier to "
                "show than to describe - and they cost tokens on every single call. "
                "In one of my demos the two examples are 50 tokens on a 107-token "
                "prompt. That is fine. It is not fine if nobody measured it."
            },
            {
                "p": "Retries are not free either, and they grow the conversation "
                "every time, because the rejected output and the correction both stay "
                "in the history. A repair loop that runs three times is a much more "
                "expensive request than the one you benchmarked."
            },
            {
                "quote": "The prompt is a request. Your schema is the guarantee. "
                "Never confuse the two."
            },
        ],
    },
    {
        "slug": "bilingual-by-default",
        "title": "Bilingual by default",
        "date": "October 2026",
        "reading": "5 min",
        "summary": (
            "Building Sattam and Mozhi for Tamil readers taught me that translation "
            "is the easy part. Order, grouping and the choice of what to include are "
            "the parts that decide whether anyone can actually use it."
        ),
        "tags": ["Tamil", "Product", "Accessibility"],
        "body": [
            {
                "p": "Sattam is a free site of everyday Indian law - traffic stops, "
                "OTP fraud, rent deposits, unpaid salary - written in plain Tamil and "
                "English. It started because the information already exists and is "
                "public. It is just written in a register most people do not read, in "
                "an order that assumes you already know which section you need."
            },
            {"h": "Tamil first, English below"},
            {
                "p": "The layout decision that mattered most was order. Each point is "
                "Tamil first, English underneath, always. Not a language switcher, "
                "not a separate page. Two reasons: a reader who is more comfortable in "
                "Tamil never has to click to get the useful version, and a reader who "
                "is more comfortable in English can use the Tamil line to check the "
                "meaning of a term they are about to sign something about."
            },
            {
                "p": "That second one turned out to matter more than I expected. "
                "People dealing with a legal document often know the English word and "
                "not the Tamil one, or the reverse. Seeing both, side by side, is the "
                "feature."
            },
            {"h": "Group by situation, not by statute"},
            {
                "p": "The obvious structure is by law: Motor Vehicles Act, Consumer "
                "Protection Act, and so on. That is how lawyers file things. It is "
                "useless if you are standing on the road being asked for your papers. "
                "So the 165 points are grouped by the situation you are in - \"a "
                "traffic officer stops you\", \"money left your account without your "
                "OTP\", \"your landlord will not return the deposit\"."
            },
            {
                "quote": "Nobody wakes up wanting to read a statute. They wake up with "
                "a problem."
            },
            {"h": "What Mozhi taught me about speech"},
            {
                "p": "Mozhi is a conversation app for Tamil and English. The "
                "assumption I had to throw out was that a conversation happens in one "
                "language. It does not. People here start a sentence in Tamil, drop "
                "into English for the technical noun, and finish back in Tamil. Any "
                "design that forces a language choice up front is already wrong."
            },
            {"h": "What I would do differently"},
            {
                "list": [
                    "Write the Tamil first, not translate it later - the sentence structure differs, and a translation reads like one",
                    "Test with someone who reads slowly, not with someone who reads fast and is being kind",
                    "Keep the source plain: no build step, no framework, nothing that can break in three years",
                    "Number the points so people can refer to them out loud",
                ]
            },
            {
                "p": "Neither site is finished. But both are usable by the person "
                "they were written for, which is more than the pages they replaced."
            },
        ],
    },
]
