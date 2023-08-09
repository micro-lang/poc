# Micro

## concepts
- `token`: keyword, name, symbol
- `block`: list of tokens and / or other blocks
- `address`: marks the location of a value
- `value`: is stored in addresses
- `operation`: +-*/

## commands
- `block_open`:
defines the beginning of a new block that stores the next tokens

- `block_close`:
commits the tokens to the block

- `keyword_add` (name)
- `keyword_rm` (name)
- `rule_add` (name, block)
- `rule_rm` (name)

- `alocate`(address, value): stores value in address
- `free`(address): frees the address
- `ignore`(block): don't run block
- `return`: stop the execution of the current block
- `exit`: exit program

## behavior
- splits tokens by `\s*` and `\n`.
- parses tokens into blocks.
- runs the main block.
- each block runs their children blocks.

## rules

- `rule` \(\w+\) `block_open` \(.*\) `block_close`  
creates a new rule with name \1 and body \2  
Ex.:
```micro
keyword variable_keyword = let
rule variable_declaration {
    match(
        variable_keyword,
        capture(var_name, name),
        "=",
        capture(var_value, value or name)
    ),
    allocate(capture.var_name, capture.var_value)
}
```

## perks
- memory is not freed by default
