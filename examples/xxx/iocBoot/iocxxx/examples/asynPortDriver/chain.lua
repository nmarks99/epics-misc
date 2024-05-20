epics = require("epics")

-- Waits for a process to complete
-- The process status is specified by the value of 'done_pv'
-- which is 1 when the process is done, and 0 when the process is not done
-- The timeout to wait for is given in seconds
function wait_process(done_pv, timeout)
    -- wait to start
    local t0 = os.time()
    while true do
        local elap = (os.time() - t0)
        if (elap >= timeout) then
            print("Error: Timeout exceeded waiting to start process")
            break
        end
        done = epics.get(done_pv)
        if done == 0 then
            print("[lua] Started!")
            break
        end
    end

    -- Wait to finish
    t0 = os.time()
    while true do
        local elap = (os.time() - t0)
        if (elap >= timeout) then
            print("Error: Timeout exceeded waiting to start process")
            break
        end
        done = epics.get(done_pv)
        if done == 1 then
            print("[lua] Done!")
            break
        end
    end
end

function play_chain(args)
    -- local done_pv = string.format("%sDone.RVAL", args.P)
    local done_pv = args.done
    local timeout = 180.0 -- 3 minutes

    epics.put(string.format("%sStartProcess",args.P), 1)
    wait_process(done_pv, timeout)    
    epics.put(string.format("%sStartProcess",args.P), 2)
    wait_process(done_pv, timeout)    
    epics.put(string.format("%sStartProcess",args.P), 3)
    wait_process(done_pv, timeout)    
    print("[lua] Chain complete!")
end
