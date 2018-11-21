<template>
  <div class="about">
    <h1>This is an about page</h1>
    <p>
      == {{isConnected}} ==
    </p>
    <p>
      == {{votes}} ==
    </p>
    <button @click="num++">UP</button>
    <button @click="num--">Down</button>
    <button @click="vote()">VOTE!</button><br/>
    <button @click="register()">Register</button>
  </div>
</template>

<script>
// @ is an alias to /src
//import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'about',
  data () {
    return {
      count: 0,
      num: 0,
    }
  },
  components: {
    //HelloWorld
  },
  computed: {
    isConnected () {
      return this.$store.state.votes.isConnected
    },
    votes () {
      return this.$store.state.votes.votes
    }
  },
  methods: {
    vote() {
      this.$socket.emit("vote",'mj',this.num,this.count++);
    },
    register() {
      this.$socket.emit("register",'jm',"Jonsso");
    }
  }
}
</script>