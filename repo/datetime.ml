# =============================================================================
# MyLang DateTime Package v1.0.0
# =============================================================================

let _datetime = __py_import__("datetime")
let _time = __py_import__("time")

# DateTime Class
export class DateTime {
    fn new(year, month, day, hour, minute, second) {
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour or 0
        self.minute = minute or 0
        self.second = second or 0
        self._dt = _datetime.datetime(year, month, day, self.hour, self.minute, self.second)
        return self
    }
    
    fn format(fmt) {
        return self._dt.strftime(fmt)
    }
    
    fn to_string() {
        return self.format("%Y-%m-%d %H:%M:%S")
    }
    
    fn add_days(days) {
        let dt = self._dt + _datetime.timedelta(days)
        return DateTime.new(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    }
    
    fn timestamp() {
        return self._dt.timestamp()
    }
    
    fn day_of_week() {
        return self._dt.weekday()
    }
    
    fn is_weekend() {
        let dow = self.day_of_week()
        return dow == 5 or dow == 6
    }
}

# Factory Functions
export fn datetime_now() {
    let now = _datetime.datetime.now()
    return DateTime.new(now.year, now.month, now.day, now.hour, now.minute, now.second)
}

export fn datetime_today() {
    let today = _datetime.date.today()
    return DateTime.new(today.year, today.month, today.day, 0, 0, 0)
}

export fn datetime_from_timestamp(ts) {
    let dt = _datetime.datetime.fromtimestamp(ts)
    return DateTime.new(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
}

export fn datetime_parse(s, fmt) {
    try {
        let dt = _datetime.datetime.strptime(s, fmt)
        return DateTime.new(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    } catch(e) {
        return none
    }
}

export fn datetime_create(year, month, day, hour, minute, second) {
    return DateTime.new(year, month, day, hour, minute, second)
}

# Utility Functions
export fn sleep(seconds) {
    _time.sleep(seconds)
}

export fn timestamp() {
    return _time.time()
}

export fn format_timestamp(ts, fmt) {
    return _datetime.datetime.fromtimestamp(ts).strftime(fmt)
}

export fn is_leap_year(year) {
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
}

export fn day_name(day_of_week) {
    let names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return names[day_of_week]
}

export fn month_name(month) {
    let names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return names[month - 1]
}
