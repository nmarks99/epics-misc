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
{M,   PORT, ADDR, PREC, SCAN}
{m1,  ACS1,    0,    6,    2}
{m2,  ACS1,    1,    6,    2}
{m3,  ACS1,    2,    6,    2}
{m4,  ACS1,    3,    6,    2}
{m5,  ACS1,    4,    6,    2}
{m6,  ACS1,    5,    6,    2}
{m7,  ACS1,    6,    6,    2}
{m8,  ACS1,    7,    6,    2}
}
]]

local lines = {}
for line in subs_file_text:gmatch("[^\r\n]+") do
    table.insert(lines, line)
end

local db_files = {}
local patterns = {}
local data = {}
local data_indices = {} -- {data start, data end}
local looking_for_data_end = 0
for i, line in ipairs(lines) do
    if line:find("file") then
        table.insert(db_files, line:match('"([^"]*)"'))
    end
    if line:find("pattern") then
        table.insert(patterns, lines[i+1])
        table.insert(data_indices, {i+2, nil})
        looking_for_data_end = 1
    end
    if looking_for_data_end > 0 then
        if looking_for_data_end > 2 then
            local line_strip = line:gsub("^%s+", ""):gsub("%s+$", "");
            if line_strip == "}" then
                data_indices[#data_indices][2] = i-1
                looking_for_data_end = 0
            end
        else
            looking_for_data_end = looking_for_data_end + 1
        end
    end
end

for i, inds in ipairs(data_indices) do
    local data_tmp = {}
    for j = inds[1], inds[2] do
        table.insert(data_tmp, lines[j])
    end
    table.insert(data, data_tmp)
end

local function new_block(file, pattern, data)
    return {
        file = file,
        pattern = pattern,
        data = data
    }
end

local blocks = {}
for i, _ in ipairs(data) do
    table.insert(blocks, new_block(db_files[i], patterns[i], data[i]))
end

for _, block in ipairs(blocks) do
    print(block.file)
    print(block.pattern)
    print(block.data)
    print("")
end

-- for i, inds in ipairs(data_indices) do
    -- io.write("File = ", db_files[i], "\n")
    -- io.write("Pattern = ", patterns[i], "\n")
    -- io.write("Data = \n")
    -- for _, data_line in ipairs(data[i]) do
        -- print(data_line)
    -- end
    -- print("\n")
-- end
