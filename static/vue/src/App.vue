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

      <!-- Team Records Table -->
      <div class="bg-white shadow-md rounded-lg p-6 mb-8">
        <h3 class="text-xl font-semibold text-[#D81D47] mb-4">Team Records</h3>
        <div class="overflow-x-auto">
          <table class="w-full table-auto">
            <thead class="bg-[#0061A1] text-white text-left">
              <tr>
                <th class="px-4 py-2"></th>
                <th class="px-4 py-2">Team</th>
                <th @click="toggleSort" class="px-4 py-2 cursor-pointer inline-flex">
                  Win % 
                  <span v-if="sortAscending" class="text-white hover:text-gray-300"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-up"><path d="m5 12 7-7 7 7"/><path d="M12 19V5"/></svg></span>
                  <span v-else class="text-white hover:text-gray-300"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-down"><path d="M12 5v14"/><path d="m19 12-7 7-7-7"/></svg></span>
                </th>
                <th class="px-4 py-2">Wins</th>
                <th class="px-4 py-2">Losses</th>
                <th class="px-4 py-2">Games Played</th>
                <th class="px-4 py-2">Home Games</th>
                <th class="px-4 py-2">Away Games</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(record, index) in sortedTeamRecords" :key="record.team_name" class="border-b">
                <td class="px-4 py-2">{{ sortAscending ? teamRecords.length - index : index + 1 }}</td>
                <td class="px-4 py-2">{{ record.team_name }}</td>
                <td class="px-4 py-2">{{ (record.win_percentage * 100).toFixed(1) }}%</td>
                <td class="px-4 py-2">{{ record.total_wins }}</td>
                <td class="px-4 py-2">{{ record.total_losses }}</td>
                <td class="px-4 py-2">{{ record.total_games_played }}</td>
                <td class="px-4 py-2">{{ record.total_home_games }}</td>
                <td class="px-4 py-2">{{ record.total_away_games }}</td>
              </tr>
            </tbody>
          </table>
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
export default {
  name: 'App',
  data() {
    return {
      teamRecords: [],
      sortAscending: false
    }
  },
  computed: {
    sortedTeamRecords() {
      return [...this.teamRecords].sort((a, b) => {
        return this.sortAscending 
          ? a.win_percentage - b.win_percentage
          : b.win_percentage - a.win_percentage;
      });
    }
  },
  mounted() {
    this.fetchTeamRecords()
  },
  methods: {
    async fetchTeamRecords() {
      try {
        const response = await fetch('/api/team-records/')
        if (!response.ok) {
          throw new Error('Network response was not ok')
        }
        this.teamRecords = await response.json()
      } catch (error) {
        console.error('Error fetching team records:', error)
      }
    },
    toggleSort() {
      this.sortAscending = !this.sortAscending;
    }
  }
}
</script>

<style>
</style>
