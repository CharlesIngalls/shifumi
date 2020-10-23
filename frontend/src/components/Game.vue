<template>
    <div v-if="is_loaded">
        <div v-if="can_play()">
            <button v-on:click="play('ROCK')">Rock</button>
            <button v-on:click="play('PAPER')">Paper</button>
            <button v-on:click="play('SCISSOR')">Scissor</button>
        </div>

        <div v-else>
            <p> You can't play for the moment. Wait for you opponent to play.</p>
        </div>

        <div>
            <div v-for="(round, i) in game.old_rounds" :key="round.id">
                <hr>
                <p>Round {{i}}: {{get_winner(round)}}</p>
                <p>Player A played {{get_choice_A(round)}}</p>
                <p>Player B played {{get_choice_B(round)}}</p>
            </div>
        </div>

    </div>
</template>

<script>
    export default {
        name: "Game",
        methods: {
            play: function (choice) {
                this.$http.post(this.$hostname + "/choices/", {
                    "choice_played": choice,
                    "access_id": this.$route.params.access_id
                }).then(() => {
                    this.load_game()
                })
            },
            load_game: function() {
                this.$http.get(this.$hostname + "/play/" + this.$route.params.access_id).then((result) => {
                    this.game = result.data
                    this.is_loaded = true
                })
            },
            get_winner: function(round) {
                if (round.is_A_winner) {
                    return "Winner A"
                } else if (round.is_draw){
                    return "Draw"
                } else {
                    return "Winner B"
                }
            },
            get_choice_A: function(round) {
                return round.choices.find(c => c.is_player_A === true).choice_played
            },
            get_choice_B: function(round) {
                return round.choices.find(c => c.is_player_A === false).choice_played
            },
            can_play: function() {
                if (parseInt(this.$route.params.access_id) === this.game.access_a) {
                    return this.game.can_A_play
                }

                if (parseInt(this.$route.params.access_id) === this.game.access_b) {
                    return this.game.can_B_play
                }

                return false // should not be possible
            }
        },
        data() {
            return {
                is_loaded: false,
                game: null,
            }
        },
        mounted() {
            if (!this.is_loaded) {
                this.load_game()
            }
        }
    }
</script>

<style scoped>

</style>
