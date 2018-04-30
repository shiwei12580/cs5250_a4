'''
CS5250 Assignment 4, Scheduling policies simulator
Sample skeleton program
Author: Minh Ho
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt
Apr 10th Revision 1:
    Update FCFS implementation, fixed the bug when there are idle time slices between processes
    Thanks Huang Lung-Chen for pointing out
Revision 2:
    Change requirement for future_prediction SRTF => future_prediction shortest job first(SJF), the simpler non-preemptive version.
    Let initial guess = 5 time units.
    Thanks Lee Wei Ping for trying and pointing out the difficulty & ambiguity with future_prediction SRTF.
'''
import sys
import copy 
input_file = 'input.txt'

class Process:
    last_scheduled_time = 0
    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
        self.predict_time = 0 # predicted process time 
        self.preempt_time = -1
        self.task_finished = False
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrive_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time
def RR_scheduling(process_list, time_quantum ):
    schedule = []
    queue = [] 
    waiting_time = 0
    current_time = 0
    ap = 0 #arrived process 
    rp = 0 # ready process 
    done = 0
    q  = time_quantum
    n = len(process_list) 
    current_proc_index = -1 # current process index
    while(done<n): 
        for i in range(ap, n): 
            if current_time >= process_list[i].arrive_time:
                queue.append(copy.deepcopy(process_list[i]))
                ap+=1
                rp+=1
        if rp<1: 
            #schedule.append((current_time, -1)) # no task, use -1 to represent idle
            current_time+=1
            continue
            
        while True: 
            #print(queue)
            #context switch to next unfinished task 
            current_proc_index +=1 
            if(current_proc_index >= len(queue)): 
                current_proc_index = 0
            
            if queue[current_proc_index].burst_time == 0: continue
            else: break
                     
        
        if queue[current_proc_index].burst_time > q: 
            schedule.append((current_time, queue[current_proc_index].id))
            if queue[current_proc_index].preempt_time == -1: #new process come, schedule for the first time 
                waiting_time = waiting_time + (current_time - queue[current_proc_index].arrive_time)
            else:   #process has been scheduled before but been preempt 
                waiting_time = waiting_time + (current_time - queue[current_proc_index].preempt_time) 
            current_time+=q
            #update preempt time to current time
            queue[current_proc_index].preempt_time = current_time
            queue[current_proc_index].burst_time-=q
        else: 
            schedule.append((current_time, queue[current_proc_index].id))
            if queue[current_proc_index].preempt_time == -1: #new process come, schedule for the first time 
                waiting_time = waiting_time + (current_time - queue[current_proc_index].arrive_time)
            else:   #process has been scheduled before but been preempt 
                waiting_time = waiting_time + (current_time - queue[current_proc_index].preempt_time) 
            current_time += queue[current_proc_index].burst_time
            #update preempt time to current time
            queue[current_proc_index].preempt_time = current_time
            queue[current_proc_index].burst_time = 0
            done += 1
            rp -= 1


 
    average_waiting_time = waiting_time/float(n)
    return schedule, average_waiting_time

def SRTF_scheduling(process_list):
    schedule = []
    queue = [] 
    waiting_time = 0
    current_time = 0
    ap = 0 #arrived process 
    rp = 0 # ready process 
    done = 0
    n = len(process_list) 
    previous_proc_index = -1 # prev process index 
    current_proc_index = -1 # current process index
    while(done<n):
        #print ("current_time ->", current_time)
        for i in range(ap, n): 
            if current_time >= process_list[i].arrive_time:
                queue.append(copy.deepcopy(process_list[i]))
                ap+=1
                rp+=1
        
        if rp<1: 
            # tick current time 
            current_time +=1
            continue
        
        #find a ready process first
        while True: 
            #context switch to next unfinished task 
            current_proc_index +=1 
            if(current_proc_index >= len(queue)): 
                current_proc_index = 0
            
            if queue[current_proc_index].burst_time == 0: continue
            else: break
        
        sp = queue[current_proc_index].burst_time
        #find the shortest process 
        for p in range(0, len(queue)): 
            if (queue[p].burst_time < sp) and (queue[p].burst_time > 0): 
                current_proc_index = p
                #print("previous_proc_index: ", previous_proc_index)                  
                #print("current_proc_index: ", current_proc_index)
                sp = queue[p].burst_time
        
        #print("current_proc_index: ", current_proc_index)
        
        if(current_proc_index != previous_proc_index):
            schedule.append((current_time,queue[current_proc_index].id))
            # print((current_time,queue[current_proc_index].id))
            if queue[current_proc_index].preempt_time == -1: #new process come, schedule for the first time 
                waiting_time = waiting_time + (current_time - queue[current_proc_index].arrive_time)
            else:   #process has been scheduled before but been preempt 
                waiting_time = waiting_time + (current_time - queue[current_proc_index].preempt_time) 
            
            #print("process: ", queue[current_proc_index])
            #print("wait time: ", waiting_time)
            
            if previous_proc_index != -1: 
                # preempt previous process. 
                queue[previous_proc_index].preempt_time = current_time # preempt previous proc                   

            queue[current_proc_index].burst_time -= 1
            if queue[current_proc_index].burst_time == 0: 
                done +=1
                rp -=1
            
        else: 
            queue[current_proc_index].burst_time -= 1
            if queue[current_proc_index].burst_time == 0: 
                done +=1
                rp -=1
                
        # set the previous proc
        previous_proc_index = current_proc_index
        # tick current time 
        current_time +=1
        
    average_waiting_time = waiting_time/float(n)
    return schedule, average_waiting_time

def cal_predict(procs, alpha): 
    n = len(procs)
    if n>0: 
        i = 0; 
        while i < n: 
            if i==0: 
                procs[0].predict_time = 5
                if procs[0].task_finished: 
                    i +=1
                    continue
                else: 
                    break
                
            if not procs[i].task_finished: # current task not finished 
                procs[i].predict_time = alpha*procs[i-1].burst_time + (1-alpha)*procs[i-1].predict_time
                break
            else: 
                i += 1
        if i>=n:  #no process available in this queue 
            return -1, 0
        else: 
            return i, procs[i].predict_time
    else:   # no process available in this  queue 
        return -1, 0

def findLeastProc(predictTime): 
    leastQueue = -1
    leastPredTime = 10000 # en choose a big number, assume no predict time is larger than this 
    for i in range(0,4): 
        if predictTime[i][0] != -1: # have proc in this queue
            if predictTime[i][1] < leastPredTime:
                leastPredTime = predictTime[i][1]
                leastQueue = i
    return leastQueue


def SJF_scheduling(process_list, alpha):
    schedule = []    
    queue = [[],[],[],[]]    
    waiting_time = 0
    current_time = 0
    ap = 0 #arrived process 
    rp = 0 # ready process 
    done = 0
    n = len(process_list) 
    while(done<n): 
        for i in range(ap, n): 
            if current_time >= process_list[i].arrive_time:
                id = process_list[i].id
                queue[id].append(copy.deepcopy(process_list[i]))
                ap+=1
                rp+=1
        if rp<1: 
            #schedule.append((current_time, -1)) # no task, use -1 to represent idle
            current_time+=1
            continue
        
        # find predict time
        predictTime = [] 
        for i in range(0,4):
            procIndex, procProdictTime = cal_predict(queue[i],alpha)
            predictTime.append((procIndex, procProdictTime))
            
        #print("predictTime: ", predictTime)        
        # find the least predict time. 
        queueIndex = findLeastProc(predictTime)
        processIndex = predictTime[queueIndex][0] 
        #print("queueIndex: ", queueIndex)
        #print("processIndex: ", processIndex) 
        
        schedule.append((current_time, queue[queueIndex][processIndex].id))
        queue[queueIndex][processIndex].task_finished = True
        waiting_time = waiting_time+(current_time-queue[queueIndex][processIndex].arrive_time)
        current_time += queue[queueIndex][processIndex].burst_time # run until process finish
        
        done += 1
        rp -= 1
        
    average_waiting_time = waiting_time/float(n)
    return schedule, average_waiting_time

def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    main(sys.argv[1:])