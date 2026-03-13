# =============================================================================
# MyLang DateTime Package v1.0.0
# =============================================================================
# Date and time utilities for MyLang
# Author: MyLang Team
# Repository: https://github.com/Botan-linux/mylang
# =============================================================================

let _datetime = __py_import__("datetime")
let _time = __py_import__("time")

# -----------------------------------------------------------------------------
# DateTime Class
# -----------------------------------------------------------------------------

class DateTime {
    fn new(year, month, day, hour, minute, second) {
        if year == none { year = 1970 }
        if month == none { month = 1 }
        if day == none { day = 1 }
        if hour == none { hour = 0 }
        if minute == none { minute = 0 }
        if second == none { second = 0 }
        
        self._dt = _datetime.datetime(year, month, day, hour, minute, second)
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        return self
    }
    
    fn format(fmt) {
        if fmt == none { fmt = "%Y-%m-%d %H:%M:%S" }
        return self._dt.strftime(fmt)
    }
    
    fn to_string() {
        return self.format()
    }
    
    fn add_days(days) {
        let new_dt = self._dt + _datetime.timedelta(days=days)
        return DateTime.new(new_dt.year, new_dt.month, new_dt.day, 
                           new_dt.hour, new_dt.minute, new_dt.second)
    }
    
    fn add_hours(hours) {
        let new_dt = self._dt + _datetime.timedelta(hours=hours)
        return DateTime.new(new_dt.year, new_dt.month, new_dt.day,
                           new_dt.hour, new_dt.minute, new_dt.second)
    }
    
    fn add_minutes(minutes) {
        let new_dt = self._dt + _datetime.timedelta(minutes=minutes)
        return DateTime.new(new_dt.year, new_dt.month, new_dt.day,
                           new_dt.hour, new_dt.minute, new_dt.second)
    }
    
    fn add_seconds(seconds) {
        let new_dt = self._dt + _datetime.timedelta(seconds=seconds)
        return DateTime.new(new_dt.year, new_dt.month, new_dt.day,
                           new_dt.hour, new_dt.minute, new_dt.second)
    }
    
    fn subtract_days(days) {
        return self.add_days(-days)
    }
    
    fn day_of_week() {
        # 0 = Monday, 6 = Sunday
        return self._dt.weekday()
    }
    
    fn day_of_year() {
        return self._dt.timetuple().tm_yday
    }
    
    fn week_of_year() {
        return self._dt.isocalendar()[1]
    }
    
    fn is_weekend() {
        let dow = self.day_of_week()
        return dow == 5 or dow == 6  # Saturday or Sunday
    }
    
    fn is_leap_year() {
        let y = self.year
        return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)
    }
    
    fn days_in_month() {
        let days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if self.month == 2 and self.is_leap_year() {
            return 29
        }
        return days_in_months[self.month - 1]
    }
    
    fn timestamp() {
        return self._dt.timestamp()
    }
    
    fn diff(other) {
        let delta = self._dt - other._dt
        return {
            "days": delta.days,
            "seconds": delta.seconds,
            "total_seconds": delta.total_seconds()
        }
    }
    
    fn is_before(other) {
        return self._dt < other._dt
    }
    
    fn is_after(other) {
        return self._dt > other._dt
    }
    
    fn equals(other) {
        return self._dt == other._dt
    }
    
    fn start_of_day() {
        return DateTime.new(self.year, self.month, self.day, 0, 0, 0)
    }
    
    fn end_of_day() {
        return DateTime.new(self.year, self.month, self.day, 23, 59, 59)
    }
    
    fn start_of_month() {
        return DateTime.new(self.year, self.month, 1, 0, 0, 0)
    }
    
    fn end_of_month() {
        return DateTime.new(self.year, self.month, self.days_in_month(), 23, 59, 59)
    }
    
    fn start_of_year() {
        return DateTime.new(self.year, 1, 1, 0, 0, 0)
    }
    
    fn end_of_year() {
        return DateTime.new(self.year, 12, 31, 23, 59, 59)
    }
}

# -----------------------------------------------------------------------------
# Factory Functions
# -----------------------------------------------------------------------------

# Get current date/time
fn datetime_now() {
    let now = _datetime.datetime.now()
    return DateTime.new(now.year, now.month, now.day, now.hour, now.minute, now.second)
}

# Get current UTC date/time
fn datetime_utc_now() {
    let now = _datetime.datetime.utcnow()
    return DateTime.new(now.year, now.month, now.day, now.hour, now.minute, now.second)
}

# Get today (midnight)
fn datetime_today() {
    let today = _datetime.date.today()
    return DateTime.new(today.year, today.month, today.day, 0, 0, 0)
}

# Create from timestamp
fn datetime_from_timestamp(ts) {
    let dt = _datetime.datetime.fromtimestamp(ts)
    return DateTime.new(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
}

# Parse date string
fn datetime_parse(str, fmt) {
    if fmt == none { fmt = "%Y-%m-%d %H:%M:%S" }
    try {
        let dt = _datetime.datetime.strptime(str, fmt)
        return DateTime.new(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    } catch(e) {
        return none
    }
}

# Parse ISO format date
fn datetime_parse_iso(str) {
    try {
        let dt = _datetime.datetime.fromisoformat(str)
        return DateTime.new(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    } catch(e) {
        return none
    }
}

# Create from components
fn datetime_create(year, month, day, hour, minute, second) {
    return DateTime.new(year, month, day, hour, minute, second)
}

# -----------------------------------------------------------------------------
# Date Only
# -----------------------------------------------------------------------------

class Date {
    fn new(year, month, day) {
        self.year = year
        self.month = month
        self.day = day
        self._date = _datetime.date(year, month, day)
        return self
    }
    
    fn format(fmt) {
        if fmt == none { fmt = "%Y-%m-%d" }
        return self._date.strftime(fmt)
    }
    
    fn to_string() {
        return self.format()
    }
    
    fn to_datetime() {
        return DateTime.new(self.year, self.month, self.day, 0, 0, 0)
    }
    
    fn add_days(days) {
        let new_date = self._date + _datetime.timedelta(days=days)
        return Date.new(new_date.year, new_date.month, new_date.day)
    }
    
    fn day_of_week() {
        return self._date.weekday()
    }
    
    fn day_of_year() {
        return self._date.timetuple().tm_yday
    }
    
    fn is_weekend() {
        let dow = self.day_of_week()
        return dow == 5 or dow == 6
    }
    
    fn diff(other) {
        let delta = self._date - other._date
        return delta.days
    }
}

fn date_today() {
    let today = _datetime.date.today()
    return Date.new(today.year, today.month, today.day)
}

fn date_create(year, month, day) {
    return Date.new(year, month, day)
}

fn date_parse(str, fmt) {
    if fmt == none { fmt = "%Y-%m-%d" }
    try {
        let d = _datetime.datetime.strptime(str, fmt).date()
        return Date.new(d.year, d.month, d.day)
    } catch(e) {
        return none
    }
}

# -----------------------------------------------------------------------------
# Time Only
# -----------------------------------------------------------------------------

class Time {
    fn new(hour, minute, second) {
        if hour == none { hour = 0 }
        if minute == none { minute = 0 }
        if second == none { second = 0 }
        
        self.hour = hour
        self.minute = minute
        self.second = second
        self._time = _datetime.time(hour, minute, second)
        return self
    }
    
    fn format(fmt) {
        if fmt == none { fmt = "%H:%M:%S" }
        return self._time.strftime(fmt)
    }
    
    fn to_string() {
        return self.format()
    }
    
    fn add_hours(hours) {
        let total_seconds = self.hour * 3600 + self.minute * 60 + self.second
        total_seconds = total_seconds + hours * 3600
        total_seconds = total_seconds % 86400  # Wrap around midnight
        let h = __py_import__("int")(total_seconds / 3600)
        total_seconds = total_seconds % 3600
        let m = __py_import__("int")(total_seconds / 60)
        let s = total_seconds % 60
        return Time.new(h, m, s)
    }
    
    fn add_minutes(minutes) {
        let total_seconds = self.hour * 3600 + self.minute * 60 + self.second
        total_seconds = total_seconds + minutes * 60
        total_seconds = total_seconds % 86400
        let h = __py_import__("int")(total_seconds / 3600)
        total_seconds = total_seconds % 3600
        let m = __py_import__("int")(total_seconds / 60)
        let s = total_seconds % 60
        return Time.new(h, m, s)
    }
    
    fn total_seconds() {
        return self.hour * 3600 + self.minute * 60 + self.second
    }
    
    fn diff(other) {
        return self.total_seconds() - other.total_seconds()
    }
}

fn time_now() {
    let now = _datetime.datetime.now().time()
    return Time.new(now.hour, now.minute, now.second)
}

fn time_create(hour, minute, second) {
    return Time.new(hour, minute, second)
}

fn time_parse(str, fmt) {
    if fmt == none { fmt = "%H:%M:%S" }
    try {
        let t = _datetime.datetime.strptime(str, fmt).time()
        return Time.new(t.hour, t.minute, t.second)
    } catch(e) {
        return none
    }
}

# -----------------------------------------------------------------------------
# Time Spans / Durations
# -----------------------------------------------------------------------------

class TimeSpan {
    fn new(days, hours, minutes, seconds) {
        if days == none { days = 0 }
        if hours == none { hours = 0 }
        if minutes == none { minutes = 0 }
        if seconds == none { seconds = 0 }
        
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self._delta = _datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        return self
    }
    
    fn total_seconds() {
        return self._delta.total_seconds()
    }
    
    fn total_minutes() {
        return self.total_seconds() / 60
    }
    
    fn total_hours() {
        return self.total_seconds() / 3600
    }
    
    fn total_days() {
        return self.total_seconds() / 86400
    }
    
    fn format(fmt) {
        if fmt == none { fmt = "{days}d {hours}h {minutes}m {seconds}s" }
        let result = fmt
        result = __py_import__("str").replace(result, "{days}", __py_import__("str")(self.days))
        result = __py_import__("str").replace(result, "{hours}", __py_import__("str")(self.hours))
        result = __py_import__("str").replace(result, "{minutes}", __py_import__("str")(self.minutes))
        result = __py_import__("str").replace(result, "{seconds}", __py_import__("str")(self.seconds))
        return result
    }
    
    fn to_string() {
        return self.format()
    }
    
    fn add(other) {
        return TimeSpan.from_seconds(self.total_seconds() + other.total_seconds())
    }
    
    fn subtract(other) {
        return TimeSpan.from_seconds(self.total_seconds() - other.total_seconds())
    }
}

fn timespan_from_seconds(seconds) {
    let days = __py_import__("int")(seconds / 86400)
    seconds = seconds % 86400
    let hours = __py_import__("int")(seconds / 3600)
    seconds = seconds % 3600
    let minutes = __py_import__("int")(seconds / 60)
    seconds = seconds % 60
    return TimeSpan.new(days, hours, minutes, __py_import__("int")(seconds))
}

fn timespan_create(days, hours, minutes, seconds) {
    return TimeSpan.new(days, hours, minutes, seconds)
}

# -----------------------------------------------------------------------------
# Utility Functions
# -----------------------------------------------------------------------------

# Sleep for seconds
fn sleep(seconds) {
    _time.sleep(seconds)
}

# Get Unix timestamp
fn timestamp() {
    return _time.time()
}

# Measure execution time
fn measure(fn) {
    let start = _time.time()
    let result = fn()
    let end = _time.time()
    return {
        "result": result,
        "duration": end - start
    }
}

# Format timestamp
fn format_timestamp(ts, fmt) {
    if fmt == none { fmt = "%Y-%m-%d %H:%M:%S" }
    return _datetime.datetime.fromtimestamp(ts).strftime(fmt)
}

# Check if year is leap year
fn is_leap_year(year) {
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
}

# Get days in month
fn days_in_month(year, month) {
    let days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if month == 2 and is_leap_year(year) {
        return 29
    }
    return days[month - 1]
}

# Get day name
fn day_name(day_of_week) {
    let names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return names[day_of_week] or ""
}

# Get month name
fn month_name(month) {
    let names = ["January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"]
    return names[month - 1] or ""
}

# Get short day name
fn day_name_short(day_of_week) {
    let names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return names[day_of_week] or ""
}

# Get short month name
fn month_name_short(month) {
    let names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return names[month - 1] or ""
}

# -----------------------------------------------------------------------------
# Export all
# -----------------------------------------------------------------------------

export DateTime
export datetime_now, datetime_utc_now, datetime_today
export datetime_from_timestamp, datetime_parse, datetime_parse_iso, datetime_create

export Date
export date_today, date_create, date_parse

export Time
export time_now, time_create, time_parse

export TimeSpan
export timespan_from_seconds, timespan_create

export sleep, timestamp, measure, format_timestamp
export is_leap_year, days_in_month
export day_name, month_name, day_name_short, month_name_short
