# Analysis

## Layer 1, Head 4

The head 4 from layer 1 seems to pay attention to up to 4 tokens that come before the token in question. Meanwhile, at times it only looks at the first token, it is often looking at more than one. It seems to be trying to get the context of a token by the tokens that came before it. 

For example, in the phrase 'We turned down a narrow lane and passed through a small [MASK].' when the token was 'Lane', it was paying attention to 'turned down a narrow', on the same phrase, on the token [MASK] it was paying attention to 'Passed through a small'.

Another example being from the phrase 'Then I picked up a [MASK] from the table.' The token 'up' is paying attention to the 'I Picked', the token [MASK] is paying attention to the tokens 'I Picked up a [MASK]' and the token 'table' is paying attention to 'from the'.

As a last example, on the phrase 'The turtle moved slowly across the [MASK]', The tokens from 'moved' all the way to the token [MASK] are looking at the 2–4 tokens that followed it. In particular, the token [Mask] is looking at 'moved slowly across the '

Example Sentences:
- We turned down a narrow lane and passed through a small [MASK].
- Then I picked up a [MASK] from the table.
- The turtle moved slowly across the [MASK].

## Layer 3, Head 2

The head 2 from layer 3 seems to be paying attention to the relationship between token in a more meaning-wise way, trying to find their meaning together or their context, whether they are coming before or after then.

In the phrase 'We made a very long trip around the country [MASK].', the token 'trip' is paying attention to the token 'Made', despite having the token 'a very long' between, meaning that head is likely trying to grasp the relationship or these tokens. Another example on the same phrase is the token 'country' that is paying a lot of attention to the token 'around'. Likely to get the meaning that this isn't a trip to just one part of the country, but a larger portion of it.

Another example being the phrase, 'This situation is far too much for any single [MASK] to bear alone.' The tokens 'far', 'much' and 'for' are paying a lot of attention to the token 'too', likely recognizing the intensity conveyed by that token. Meanwhile, the token 'single' is paying attention to both 'any' and [MASK], meaning it's getting that this 'single' is modifying the meaning of 'any [MASK]'; the token [MASK] is paying attention to 'any single' that modifies it and the tokens 'to' and 'bear' are paying attention to [MASK], while the token 'alone' is paying attention to both '[MASK]' and 'bear', this means the model is getting the semantic relationship between these words.

Example Sentences:
- We made a very long trip around the country [MASK].
- This situation is far too much for any single [MASK] to bear alone.

## Layer 2, Head 7

The head 7 from layer 2 seems to be paying to the tokens that modify nouns.

An example of that is the phrase, 'This situation is far too much for any single [MASK] to bear alone.'. The tokens 'for any single' and 'bear alone' are all paying a lot of attention to the token [Mask], meaning the model is recognizing these tokens as modifiers of the noun that '[MASK]' represents.

Another example that shows this is the phrase 'He is a straightforward and caring [MASK], although quite greedy.', the tokens 'straightforward and caring [MASK]' and 'although quite' all pay a lot of attention to [Mask]. Since both phrases refer and modify [MASK], it reinforces the view that it's looking for tokens that modify nouns. One thing that eludes me in this example, is the fact that on that phrase, the token 'greedy' pays attention to 'quite greedy.' instead of [Mask], one possible answer is that it recognizes 'quite greedy' as a phrase that modifies the noun, so it's paying attention to how that phrase modifies the noun, rather than the noun itself.

Example Sentences:
- This situation is far too much for any single [MASK] to bear alone.
- He is a straightforward and caring [MASK], although quite greedy.