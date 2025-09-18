#!/usr/bin/env lua

local function strip_whitespace(str)
    local cleaned = str:gsub("^%s+", ""):gsub("%s+$", "")
    return cleaned
end

local function max_table(t1, t2)
    assert(#t1 == #t2, "tables must be the same length")
    local tout = {}
    for i = 1, #t1 do
	tout[i] = t1[i] > t2[i] and t1[i] or t2[i]
    end
    return tout
end

local function parse(text)
    -- get start and end indices of data sections
    local lines = {}
    for line in text:gmatch("[^\r\n]+") do
	table.insert(lines, line)
    end

    local data_lines = {}
    local col_widths = {}
    local i_data = 0
    local in_data_block = false
    for i, line in ipairs(lines) do
	data_lines[i] = false
	if in_data_block then
	    if strip_whitespace(line) == "}" then
		in_data_block = false
		data_lines[i] = false
	    else
		data_lines[i] = true
		local col_widths_i = {}
		for field in line:gmatch("[^,{}]+") do
		    local len = #strip_whitespace(field)
		    table.insert(col_widths_i, len)
		end
		if col_widths[i_data] then
		    col_widths[i_data] =  max_table(col_widths_i, col_widths[i_data])
		else
		    col_widths[i_data] =  col_widths_i
		end
	    end
	end

	if line:find("pattern") then
	    in_data_block = true
	    i_data = i_data + 1
	end
    end

    return  {
	lines = lines,
	data_lines = data_lines,
	col_widths = col_widths
    }
end

local function format(subs_file_content)
    local subs = parse(subs_file_content)
    local formatted_text = ""

    local i_data = 1
    local in_data_block = false
    for i, line in ipairs(subs.lines) do
	if subs.data_lines[i] then
	    in_data_block = true

	    -- get all the fields and strip the leading/trailing whitespace
	    local fields = {}
	    for f in line:gmatch("[^,{}]+") do
		table.insert(fields, strip_whitespace(f))
	    end

	    -- build the formatting string for this line
	    formatted_text = formatted_text .. "{"
	    for j, field in ipairs(fields) do
		local pad = string.rep(" ", subs.col_widths[i_data][j] - #field)
		formatted_text = formatted_text .. pad .. field
		if j == #fields then
		    formatted_text = formatted_text .. "}"
		else
		    formatted_text = formatted_text .. ",  "
		end
	    end
	    formatted_text = formatted_text .. "\n"
	else
	    -- if this isn't a data line, just add the line as is
	    formatted_text = formatted_text .. line
	    -- update the indices and flags, add new lines as needed
	    local new_lines = 0
	    if in_data_block then
		i_data = i_data + 1
		if i ~= #subs.lines then
		    new_lines = new_lines + 1
		end
	    end
	    if i ~= #subs.lines then
		new_lines = new_lines + 1
	    end
	    formatted_text = formatted_text .. string.rep("\n", new_lines)
	    in_data_block = false
	end
    end

    return formatted_text
end

-- local file_contents = io.read("*all")
-- if not file_contents or #file_contents == 0 then
    -- print("No input provided")
    -- os.exit(1)
-- end
-- print(format(file_contents))

local file_contents
if #arg >= 1 then
    -- Read from the file passed as an argument
    local filename = arg[1]
    local f, err = io.open(filename, "r")
    if not f then
        io.stderr:write("Error opening file: " .. err .. "\n")
        os.exit(1)
    end
    file_contents = f:read("*all")
    f:close()
else
    io.stderr:write("Error: no input provided\n")
    os.exit(1)
end

print(format(file_contents))
