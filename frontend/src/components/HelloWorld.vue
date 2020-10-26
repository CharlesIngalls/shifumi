<template>
    <div class="main">
        <button v-on:click="create_game">New Game</button>
        <p>First player to win 3 rounds wins the game.</p>
        <div v-if="is_game_created" class="url_sessions">
            <p>You're the player A. Use this link: <a :href="this.$domain + '/' + access_a">{{this.$domain + '/' + access_a}}</a></p>
            <p>Send this link to the player B:  <a :href="this.$domain + '/' + access_b">{{this.$domain + '/' + access_b}}</a></p>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'HelloWorld',
        data() {
            return {
                access_a: null,
                access_b: null,
                is_game_created: false
            }
        },
        methods: {
            create_game: function () {
                this.$http.post(this.$hostname + "/games/").then((result) => {
                    this.access_a = result.data.access_a
                    this.access_b = result.data.access_b
                    this.is_game_created = true
                })
            }
        },
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    h3 {
        margin: 40px 0 0;
    }

    ul {
        list-style-type: none;
        padding: 0;
    }

    li {
        display: inline-block;
        margin: 0 10px;
    }

    a {
        color: #42b983;
    }
</style>
