# great-again

A late-night spin on Donald Trump's presidential campaign. Go to [greataga.in](http://greataga.in)
to see it in action.

### How it works

1. On `/<term>`, we use the Yahoo! BOSS Search API to find matching images.
2. Once we have a candidate set, we filter on size and type and start downloading the
images asynchronously in batches of 3 until the first image that can be read successfully.
3. We then feed the image to the `draw` module which calculates the appropriate font size
based on the term length and creates the image.
4. The image is then uploaded on S3.
5. For obvious performance reasons, we cache the result per term.

### Example

[greataga.in/java](http://greataga.in/java)

![Cats](http://great-again.s3.amazonaws.com/v8gRCBQ8ewmQjpQy7FZJUW.jpg)
