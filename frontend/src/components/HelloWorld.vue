<template>
  <div v-if="eorzeaTime">
    <span> ET: {{ formatTime(eorzeaTime) }} </span>
    <span> LT: {{ formatDate(getLocalTime(eorzeaTime.totalSeconds)) }} {{ formatTime(getLocalTime(eorzeaTime.totalSeconds)) }} </span>
    <div v-for="(place, index) in data.place_list" v-bind:key="'place:' + index">
      <div>
        <span> {{ data.lang_data.place[place[0]] }} </span>
        <span> {{ data.lang_data.place[place[1]] }} </span>
      </div>
      <div v-for="(time, idx) in weatherTimes" v-bind:key="'weather:' + index + '-' + idx">
        <span> ET: {{ formatTime(time.et) }} </span>
        <span> Weather: {{ data.lang_data.weather[getWeatherId(time.et.totalSeconds, place[2])] }} </span>
        <span> LT: {{ formatDate(time.lt) }} {{ formatTime(time.lt) }} </span>
      </div>
    </div>
  </div>
</template>

<script>
import DataContainer from '@/assets/data'

// const MOON_SPAN = 86400 * 4
const WEATHER_SPAN = 3600 * 8
const YEAR_SPAN = 86400 * 384
const MONTH_SPAN = 86400 * 32
const WEEK_SPAN = 86400 * 8
const DAY_SPAN = 86400
// const DAY_QUARTER_SPAN = 3600 * 6
const HOUR_SPAN = 3600
const MINUTE_SPAN = 60

export default {
  // name: 'HelloWorld',
  data () {
    return {
      data: DataContainer,
      eorzeaTime: null,
      startWeatherTime: 0
    }
  },
  computed: {
    weatherTimes () {
      const nums = 3 * 5
      const times = Array(nums)
      for (var i = 0; i < nums; ++i) {
        const t = this.startWeatherTime + WEATHER_SPAN * i
        times[i] = {
          et: this.getEorzeaTime(t),
          lt: this.getLocalTime(t)
        }
      }
      return times
    }
  },
  mounted () {
    setInterval(() => {
      const eorzeaTimeSec = this.convertToEorzeaTime(new Date().getTime() / 1000)
      const newMinutes = (eorzeaTimeSec / MINUTE_SPAN) >>> 0
      const oldMinutes = (((!!this.eorzeaTime && this.eorzeaTime.totalSeconds) || 0) / MINUTE_SPAN) >>> 0
      if (newMinutes !== oldMinutes) {
        this.eorzeaTime = this.getEorzeaTime(eorzeaTimeSec)

        const nowWeatherTime = parseInt(eorzeaTimeSec - (eorzeaTimeSec % WEATHER_SPAN))
        if (this.startWeatherTime !== nowWeatherTime) {
          this.startWeatherTime = nowWeatherTime
        }
      }
    }, 300)
  },
  methods: {
    convertToEorzeaTime (unixSec) {
      return unixSec * (1440.0 / 70.0)
    },
    convertToUnixTime (eorzeaSec) {
      return eorzeaSec * (70.0 / 1440.0)
    },
    getEorzeaTime (eorzeaTimeSec) {
      const t = eorzeaTimeSec
      const hours = parseInt((t / HOUR_SPAN) % 24)
      return {
        year: parseInt(t / YEAR_SPAN + 1),
        month: parseInt((t / MONTH_SPAN + 1) % 32),
        day: parseInt((t / DAY_SPAN + 1) % 32),
        week: parseInt((t / WEEK_SPAN) % 8),
        hours_quorter: parseInt((t / HOUR_SPAN) % 4),
        hours: hours,
        hour_attr: parseInt(hours % 6),
        minutes: parseInt((t / MINUTE_SPAN) % 60),
        seconds: parseInt(t % 60),
        totalSeconds: t
      }
    },
    getLocalTime (eorzeaTimeSec) {
      const date = new Date(this.convertToUnixTime(eorzeaTimeSec) * 1000)
      return {
        year: date.getYear(),
        month: date.getMonth() + 1,
        day: date.getDate(),
        week: date.getDay(),
        hours: date.getHours(),
        minutes: date.getMinutes(),
        seconds: date.getSeconds(),
        totalSeconds: date.getTime() / 1000
      }
    },
    formatDate (t) {
      return (t.month < 10 ? '0' : '') + t.month + '-' + (t.day < 10 ? '0' : '') + t.day
    },
    formatTime (t) {
      return (t.hours < 10 ? '0' : '') + t.hours + ':' + (t.minutes < 10 ? '0' : '') + t.minutes
    },
    getWeatherId (eorzeaTimeSec, weatherRateId) {
      const weatherRate = this.data.weather_rate_list[weatherRateId]
      const weathers = weatherRate[0]
      const weatherRates = weatherRate[1]
      const wt = parseInt(eorzeaTimeSec - (eorzeaTimeSec % WEATHER_SPAN))
      const days = parseInt(wt / DAY_SPAN)
      const hour = parseInt(wt / HOUR_SPAN) % 24
      const base = (days * 100) + ((hour + 8) % 24)
      const step1 = ((base << 11) ^ base) & 0xffffffff
      const step2 = ((step1 >> 8) ^ step1) & 0xffffffff
      const rate = step2 % 100
      var threshold = 0
      for (var n = 0; n < 5; ++n) {
        threshold += weatherRates[n]
        if (rate < threshold) {
          return weathers[n]
        }
      }
      return 0
    }
  }
}
</script>

<style scoped>
</style>
