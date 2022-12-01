import time
from codecarbon import EmissionsTracker

def any_func_with_loop():

    list_to_loop = [i for i in range(333)]
    t_start = time.perf_counter()
    percentage_counter = 0
    loop_counter = 0

    for item in list_to_loop:

        time.sleep(0.3)

        loop_counter+=1
        percentage = round(100*(loop_counter)/len(list_to_loop),0)
        if percentage%10==0:
            if percentage_counter !=percentage:
                t_prov=time.perf_counter()
                time_elapsed=t_prov-t_start
                time_estimated=(100*time_elapsed/percentage)-time_elapsed
                print(f'Status: {percentage:.0f}% Completed! ->'
                      f'Elapsed time: {time_elapsed: .2f}s or {time_estimated/60:.2f}min')
                percentage_counter=percentage

for y in range(1):
    for x in range(333):
        emissions_tracker = EmissionsTracker(project_name='emissions_app_reboot'+str(y))
        emissions_tracker.start()

        any_func_with_loop

        emissions_tracker.stop()
