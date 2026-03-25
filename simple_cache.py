import os
from m5.objects import *

# ------------------- System Setup -------------------
system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

system.cpu = TimingSimpleCPU()

# ------------------- Cache Configuration -------------------
system.cpu.icache = Cache(
    size='16kB',
    assoc=4,
    tag_latency=2,
    data_latency=2,
    response_latency=2,
    mshrs=4,
    tgts_per_mshr=20
)

system.cpu.dcache = Cache(
    size='16kB',
    assoc=256,
    tag_latency=2,
    data_latency=2,
    response_latency=2,
    mshrs=4,
    tgts_per_mshr=20
)

# Replacement policy for your experiments
system.cpu.dcache.replacement_policy = LRURP()

system.membus = SystemXBar()

# Connect caches
system.cpu.icache.cpu_side = system.cpu.icache_port
system.cpu.dcache.cpu_side = system.cpu.dcache_port
system.cpu.icache.mem_side = system.membus.cpu_side_ports
system.cpu.dcache.mem_side = system.membus.cpu_side_ports

# x86 interrupt controller (required)
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

# ------------------- Memory Controller -------------------
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# ------------------- Workload Setup -------------------
binary = "./test"

if not os.path.exists(binary):
    print(f"ERROR: Binary '{binary}' not found!")
    exit(1)

print(f"Using binary: {binary}")

system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]          # You can add arguments here, e.g. [binary, "arg1", "arg2"]
system.cpu.workload = process
system.cpu.createThreads()

# ------------------- Simulation -------------------
root = Root(full_system=False, system=system)

m5.instantiate()

print("Starting simulation...")
exit_event = m5.simulate()
print("Exiting @ tick", m5.curTick())