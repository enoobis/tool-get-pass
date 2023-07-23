import win32evtlog
import win32evtlogutil
import winerror
import os

def get_system_logs(log_type="System", num_records=10):
    event_log = win32evtlog.OpenEventLog(None, log_type)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    events = []
    
    try:
        total_records = win32evtlog.GetNumberOfEventLogRecords(event_log)
        records_to_read = min(total_records, num_records)
        while records_to_read > 0:
            events_batch = win32evtlog.ReadEventLog(event_log, flags, 0)
            for event in events_batch:
                event_id = winerror.HRESULT_CODE(event.EventID)
                event_category = event.EventCategory
                event_data = win32evtlogutil.SafeFormatMessage(event, log_type)
                events.append({
                    'Event ID': event_id,
                    'Event Category': event_category,
                    'Event Data': event_data,
                })
                records_to_read -= 1
                if records_to_read == 0:
                    break
    finally:
        win32evtlog.CloseEventLog(event_log)
    return events

def main():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_directory, 'system_logs.txt')

    num_records = 10
    system_logs = get_system_logs(log_type="System", num_records=num_records)

    with open(output_file, 'w') as file:
        file.write(f"------ Last {num_records} System Log Entries ------\n")
        for log_entry in system_logs:
            file.write(f"Event ID: {log_entry['Event ID']}\n")
            file.write(f"Event Category: {log_entry['Event Category']}\n")
            file.write(f"Event Data: {log_entry['Event Data']}\n")
            file.write('\n')

    print(f"System logs saved to {output_file}")

if __name__ == "__main__":
    main()