<template>
  <div>
    <div v-if="eorzeaTime">
      <span> ET: {{ formatTime(eorzeaTime) }} </span>
    </div>
    <div v-if="regionIds">
      <div v-for="regionId in regionIds" v-on:click="onSelectedRegion(regionId)" v-bind:key="'region:' + regionId">
        {{ lib.getPlaceName(regionId) }}
      </div>
    </div>
    <div v-if="selectedPlaces">
      <div v-for="(rateId, placeId) in selectedPlaces" v-bind:key="'place:' + placeId">
        {{ lib.getPlaceName(placeId) }}
        <div v-for="(time, idx) in weatherTimes" v-bind:key="'weather:' + placeId + '-' + idx">
          <span> ET: {{ formatTime(time.et) }} </span>
          <span> Weather: {{ lib.getWeatherName(lib.getWeatherId(time.et.totalSeconds, rateId)) }} </span>
          <span> LT: {{ formatDate(time.lt) }} {{ formatTime(time.lt) }} </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import WeatherForecast from '@/libWeatherForecast'

export default {
  // name: 'HelloWorld',
  data () {
    return {
      regionIds: [],
      selectedPlaces: [],
      eorzeaTime: null,
      startWeatherTime: 0
    }
  },
  computed: {
    lib: {
      get () {
        return WeatherForecast
      }
    },
    weatherTimes () {
      // const nums = 432
      const nums = 3 * 8
      return WeatherForecast.getWeatherTimes(this.startWeatherTime, nums)
    }
  },
  mounted () {
    this.regionIds = WeatherForecast.getRegions()
    this.selectedPlaces = WeatherForecast.getPlaces(this.regionIds[0])

    setInterval(() => {
      const eorzeaTimeSec = WeatherForecast.convertToEorzeaTime(new Date().getTime() / 1000)
      const newMinutes = (eorzeaTimeSec / WeatherForecast.MINUTE_SPAN) >>> 0
      const oldMinutes = (((!!this.eorzeaTime && this.eorzeaTime.totalSeconds) || 0) / WeatherForecast.MINUTE_SPAN) >>> 0
      if (newMinutes !== oldMinutes) {
        this.eorzeaTime = WeatherForecast.getEorzeaTime(eorzeaTimeSec)

        const nowWeatherTime = WeatherForecast.resolveWeatherTime(eorzeaTimeSec)
        if (this.startWeatherTime !== nowWeatherTime) {
          this.startWeatherTime = nowWeatherTime
        }
      }
    }, 300)
  },
  methods: {
    formatDate (t) {
      return (t.month < 10 ? '0' : '') + t.month + '-' + (t.day < 10 ? '0' : '') + t.day
    },
    formatTime (t) {
      return (t.hours < 10 ? '0' : '') + t.hours + ':' + (t.minutes < 10 ? '0' : '') + t.minutes
    },
    onSelectedRegion (regionId) {
      this.selectedPlaces = WeatherForecast.getPlaces(regionId)
    }
  }
}
</script>

<style scoped>
</style>
