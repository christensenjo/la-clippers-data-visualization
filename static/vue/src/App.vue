<template>
  <div id="app" class="min-h-screen bg-gray-100">
    <!-- Header -->
    <header class="bg-[#1A1919] text-white shadow-md">
      <div class="container mx-auto px-4 py-3 flex justify-between items-center">
        <h1 class="text-2xl font-bold">LA Clippers Basketball Full Stack Developer</h1>
        <nav>
          <ul class="flex space-x-4">
            <li><a href="#" class="hover:text-[#D81D47] transition-colors">Questionnaire</a></li>
            <li><a href="#" class="hover:text-[#D81D47] transition-colors">Instructions</a></li>
          </ul>
        </nav>
      </div>
    </header>

    <!-- Main content -->
    <main class="container mx-auto px-4 py-8">
      <p class="text-gray-600 text-center mb-8 max-w-3xl mx-auto">Welcome to my application! You can view my questionaire answers 
      at the link in the navbar, and examine my SQL query results and data visualizations below! If you somehow haven't seen them 
      yet, instructions for using this application are also linked above.</p>

      <!-- Month Filter -->
      <div class="mb-4">
        <label for="month-select" class="mr-2">Filter by month:</label>
        <select id="month-select" v-model="selectedMonth" @change="fetchTeamRecords" class="p-2 border rounded">
          <option value="">All Time</option>
          <option v-for="month in availableMonths" :key="month.value" :value="month.value">
            {{ month.label }}
          </option>
        </select>
      </div>

      <!-- Team Records Table -->
      <div class="bg-white shadow-md rounded-lg p-6 mb-8">
        <h3 class="text-xl font-semibold text-[#D81D47] mb-4">Team Records</h3>
        <p class="text-gray-400 mb-4">Click on a column header to rank by that column.</p>
        <div class="overflow-x-auto">
          <table class="w-full table-auto">
            <thead class="bg-[#0061A1] text-white text-left">
              <tr>
                <th class="px-4 py-2"></th>
                <th class="px-4 py-2">Team</th>
                <th @click="toggleSort('win_percentage')" class="px-4 py-2 cursor-pointer hover:text-slate-300">
                  Win % 
                  <SortIcon v-if="sortColumn === 'win_percentage'" :active="sortColumn === 'win_percentage'" :ascending="sortAscending" />
                </th>
                <th class="px-4 py-2">Wins</th>
                <th class="px-4 py-2">Losses</th>
                <th @click="toggleSort('total_home_games')" class="px-4 py-2 cursor-pointer hover:text-slate-300">
                  Home Games
                  <SortIcon v-if="sortColumn === 'total_home_games'" :ascending="sortAscending" :active="sortColumn === 'home'" />
                </th>
                <th @click="toggleSort('total_away_games')" class="px-4 py-2 cursor-pointer hover:text-slate-300">
                  Away Games
                  <SortIcon v-if="sortColumn === 'total_away_games'" :ascending="sortAscending" :active="sortColumn === 'away'" />
                </th>
                <th @click="toggleSort('total_games_played')" class="px-4 py-2 cursor-pointer hover:text-slate-300">
                  Games Played
                  <SortIcon v-if="sortColumn === 'total_games_played'" :ascending="sortAscending" :active="sortColumn === 'games'" />
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(record, index) in sortedTeamRecords" :key="record.team_name" class="border-b">
                <td class="px-4 py-2 font-bold">{{ index + 1 }}</td>
                <td class="px-4 py-2">{{ record.team_name }}</td>
                <td class="px-4 py-2">{{ (record.win_percentage * 100).toFixed(1) }}%</td>
                <td class="px-4 py-2">{{ record.total_wins }}</td>
                <td class="px-4 py-2">{{ record.total_losses }}</td>
                <td class="px-4 py-2">{{ record.total_home_games }}</td>
                <td class="px-4 py-2">{{ record.total_away_games }}</td>
                <td class="px-4 py-2">{{ record.total_games_played }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <!-- SQL Query Section -->
        <div class="mt-4">
          <button @click="toggleSqlQuery" class="flex items-center text-[#0061A1] hover:text-[#D81D47] transition-colors">
            <span class="mr-2">{{ showSqlQuery ? '▼' : '▶' }}</span>
            <span>See SQL Query</span>
          </button>
          <transition name="expand">
            <pre v-if="showSqlQuery" class="mt-2 p-4 bg-gray-100 rounded-md overflow-x-auto text-black">
              <code>{{ sqlQuery }}</code>
            </pre>
          </transition>
        </div>
      </div>

      <!-- Placeholder for SQL query results -->
      <div class="bg-white shadow-md rounded-lg p-6 mb-8">
        <h3 class="text-xl font-semibold text-[#D81D47] mb-4">SQL Query Results</h3>
        <div class="overflow-x-auto">
          <table class="w-full table-auto">
            <thead class="bg-[#0061A1] text-white">
              <tr>
                <th class="px-4 py-2">Column 1</th>
                <th class="px-4 py-2">Column 2</th>
                <th class="px-4 py-2">Column 3</th>
              </tr>
            </thead>
            <tbody>
              <tr class="border-b">
                <td class="px-4 py-2">Data 1</td>
                <td class="px-4 py-2">Data 2</td>
                <td class="px-4 py-2">Data 3</td>
              </tr>
              <!-- Add more rows as needed -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- Placeholder for data visualizations -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="bg-white shadow-md rounded-lg p-6">
          <h3 class="text-xl font-semibold text-[#D81D47] mb-4">Data Visualization 1</h3>
          <div class="aspect-w-16 aspect-h-9 bg-gray-200 rounded-md"></div>
        </div>
        <div class="bg-white shadow-md rounded-lg p-6">
          <h3 class="text-xl font-semibold text-[#D81D47] mb-4">Data Visualization 2</h3>
          <div class="aspect-w-16 aspect-h-9 bg-gray-200 rounded-md"></div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import SortIcon from './components/SortIcon.vue'
import { ref } from 'vue';

export default {
  name: 'App',
  components: {
    SortIcon
  },
  setup() {
    const showSqlQuery = ref(false);
    const sqlQuery = ref('');
    const selectedMonth = ref('');
    const availableMonths = ref([]);

    return {
      showSqlQuery,
      sqlQuery,
      selectedMonth,
      availableMonths,
    };
  },
  data() {
    return {
      teamRecords: [],
      sortColumn: 'win_percentage',
      sortAscending: false,
    }
  },
  computed: {
    sortedTeamRecords() {
      return [...this.teamRecords].sort((a, b) => {
        const modifier = this.sortAscending ? 1 : -1;
        if (a[this.sortColumn] < b[this.sortColumn]) return -1 * modifier;
        if (a[this.sortColumn] > b[this.sortColumn]) return 1 * modifier;
        return 0;
      });
    }
  },
  mounted() {
    this.fetchAvailableMonths();
    this.fetchTeamRecords();
    this.fetchSqlQuery();
  },
  methods: {
    async fetchAvailableMonths() {
      try {
        const response = await fetch('/api/available-months/');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        this.availableMonths = await response.json();
      } catch (error) {
        console.error('Error fetching available months:', error);
      }
    },
    async fetchTeamRecords() {
      try {
        let url = '/api/team-records/';
        if (this.selectedMonth) {
          const [year, month] = this.selectedMonth.split('-');
          url += `?year=${year}&month=${month}`;
        }
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        this.teamRecords = await response.json();
      } catch (error) {
        console.error('Error fetching team records:', error);
      }
    },
    async fetchSqlQuery() {
      try {
        let url = '/api/team-records-sql/';
        if (this.selectedMonth) {
          const [year, month] = this.selectedMonth.split('-');
          url += `?year=${year}&month=${month}`;
        }
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        this.sqlQuery = data.sql_query;
      } catch (error) {
        console.error('Error fetching SQL query:', error);
      }
    },
    toggleSort(column) {
      if (this.sortColumn === column) {
        this.sortAscending = !this.sortAscending;
      } else {
        this.sortColumn = column;
        this.sortAscending = false;
      }
    },
    toggleSqlQuery() {
      this.showSqlQuery = !this.showSqlQuery;
    }
  }
}
</script>

<style>
.expand-enter-active,
.expand-leave-active {
  transition: max-height 0.3s ease-in-out;
  overflow: hidden;
}

.expand-enter-from,
.expand-leave-to {
  max-height: 0;
}

.expand-enter-to,
.expand-leave-from {
  max-height: 1000px; /* Adjust this value based on your content */
}
</style>
