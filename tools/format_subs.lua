local subs_file_text = [[
file "$(MOTOR)/db/asyn_motor_model2.db"
{
pattern
{N,  M,      ADDR,  DESC,          EGU,    DIR,  VELO,  VBAS,  ACCL,  BDST,  BVEL,  BACC,  MRES,  PREC, DHLM, DLLM, INIT}
{1,  "m$(N)",  0,  "h1",    mm,  Pos,  1,     .1,    .2,    0,     1,     .2,    0.01,  5, 100, -100, ""}
{2,  "m$(N)",  1,  "h2",    mm,  Pos,  1,     .1,    .2,    0,     1,     .2,    0.01,  5, 100, -100, ""}
{3,  "m$(N)",  2,  "h3",    mm,  Pos,  1,     .1,    .2,    0,     1,     .2,    0.01,  5, 100, -100, ""}
{4,  "m$(N)",  3,  "h4",    mm,  Pos,  1,     .1,    .2,    0,     1,     .2,    0.01,  5, 100, -100, ""}
{5,  "m$(N)",  4,  "b1",    mm,  Pos,  1,     .1,    .2,    0,     1,     .2,    0.01,  5, 100, -100, ""}
{6,  "m$(N)",  5,  "b2",    mm,  Pos,  1,     .1,    .2,    0,     1,     .2,    0.01,  5, 100, -100, ""}
{7,  "m$(N)",  6,  "b3",    mm,  Pos,  1,     .1,    .2,    0,     1,     .2,    0.01,  5, 100, -100, ""}
{8,  "m$(N)",  7,  "b4",    mm,  Pos,  1,     .1,    .2,    0,     1,     .2,    0.01,  5, 100, -100, ""}
{9,  "m$(N)",  8,  "Motor $(N)",    mm,  Pos,  1,     .1,    .2,    0,     1,     .2,    0.01,  5, 100, -100, ""}
{10,  "m$(N)", 9,  "Motor $(N)",    mm,  Pos,  1,     .1,    .2,    0,     1,     .2,    0.01,  5, 100, -100, ""}
{11,  "m$(N)", 10,  "Motor $(N)",    mm,  Pos,  1,     .1,    .2,    0,     1,     .2,    0.01,  5, 100, -100, ""}
{12,  "m$(N)", 11,  "Motor $(N)",    mm,  Pos,  1,     .1,    .2,    0,     1,     .2,    0.01,  5, 100, -100, ""}
{13,  "m$(N)", 12,  "Motor $(N)",    mm,  Pos,  1,     .1,    .2,    0,     1,     .2,    0.01,  5, 100, -100, ""}
{14,  "m$(N)", 13,  "Motor $(N)",    mm,  Pos,  1,     .1,    .2,    0,     1,     .2,    0.01,  5, 100, -100, ""}
{15,  "m$(N)", 14,  "Motor $(N)",    mm,  Pos,  1,     .1,    .2,    0,     1,     .2,    0.01,  5, 100, -100, ""}
{16,  "m$(N)", 15,  "Motor $(N)",    mm,  Pos,  1,     .1,    .2,    0,     1,     .2,    0.01,  5, 100, -100, ""}
}

## The feedback database is helpful for troubleshooting encoder problems
file "$(TOP)/db/SPiiPlusFeedback.db"
{
pattern
{M,   PORT, ADDR,        PREC, SCAN}
{m1,    ACS1,    0,    6,    2}
{m2,  ACS1,    1,    6,    2}
{m3,   ACS1,    2,       6,    2}
{m4,  ACS1,    3,     6,    2}
{m5,ACS1,    4,        6,    2}
{m6,  ACS1,        5    ,    6,    2}
{m7,             ACS1,     6,        6,    2}
{m8,    ACS1,7,6,2}
}
]]


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

-- get start and end indices of data sections
local lines = {}
for line in subs_file_text:gmatch("[^\r\n]+") do
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
	    -- col_widths[i] =  col_widths_i
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

local i_data = 1
local in_data_block = false
for i, line in ipairs(lines) do
    if data_lines[i] then
	in_data_block = true
	local j = 1
	io.write("{")
	for field in line:gmatch("[^,{}]+") do
	    local pad = string.rep(" ", col_widths[i_data][j] - #strip_whitespace(field))
	    io.write(pad .. strip_whitespace(field) .. ",  ")
	    j = j + 1
	end
	-- io.write("    ")
	-- for _, v in ipairs(col_widths[i_data]) do
	    -- io.write(v, ",")
	-- end
	io.write("\n")
    else
	if in_data_block then
	    i_data = i_data + 1
	end
	in_data_block = false
    end
end
