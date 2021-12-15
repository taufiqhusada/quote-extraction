OPEN_CURLY_QUOTE = '“'
CLOSE_CURLY_QUOTE = '”'
SINGLE_QUOTE = "'"
OPEN_WEIRD_QUOTE = '``'
CLOSE_WEIRD_QUOTE = "''"


def transform_all_quotes_to_straight_double_quotes(s):
    result_text = ""
    len_s = len(s)
    skip_next_char = False
    for i in range(len_s):
        if (skip_next_char):
            skip_next_char = False
            continue
            
        if (s[i]==OPEN_CURLY_QUOTE or s[i]==CLOSE_CURLY_QUOTE):
            result_text += '"'
        elif ((i < len_s-1) and (s[i:i+2]==OPEN_WEIRD_QUOTE or s[i:i+2]==CLOSE_WEIRD_QUOTE)):
            result_text += '"'
            skip_next_char = True
        elif (s[i]==SINGLE_QUOTE and ((i==0) or (i==len_s-1) or (i>0 and s[i-1]==' ') or (i<len_s-1 and s[i+1]==' '))):
            result_text += '"'
        else:
            result_text += s[i]
    return result_text
            
if __name__ == "__main__":
    s = "'Few players reached or will ever reach the special level of Vince Wilfork,' Pats coach Bill Belichick said."
    print(transform_all_quotes_to_straight_double_quotes(s))
    s = "``this is a quote'' fabian said"
    print(transform_all_quotes_to_straight_double_quotes(s))
    s = "“this is a quote with curly quote”"
    print(transform_all_quotes_to_straight_double_quotes(s))
    s = "'Few players reached or will ever reach the special level of Vince Wilfork,' Pats coach Bill Belichick said. ``this is a quote'' fabian said “this is a quote with curly quote”"
    print(transform_all_quotes_to_straight_double_quotes(s))