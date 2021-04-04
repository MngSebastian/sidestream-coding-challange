<template>
  <!--I did not mean for the webiste to scroll down a little but for some reason nothing else besides h-screen works
  and since i have some margin above, the page gets pushed down a little.
  (tried other height classes and none worked, could probably fix this with overflow but i decided not to.) -->
  
  <div class="bckg-img h-screen flex flex-col justify-center">
    <div class="flex justify-center">

      <!--X is Undo button -->
      <div v-on:click="undoOnClick()" class="flex justify-center mt-2 text-2xl w-8 cursor-pointer">
        <img  src="https://pics.freeicons.io/uploads/icons/png/14542101961537356034-512.png" alt="Undo" />
      </div>
      
    </div>
    <div class="h-screen overflow-hidden mb-1 flex flex-row justify-around mt-2">

    <div class=" tracking-wide pt-5 flex flex-col rounded-lg shadow-2xl w-1/4 " style="backdrop-filter: blur(20px)">
      <h1 class="text-2xl font-medium pb-5 flex justify-center">Resolved</h1>
      <hr>
      <div class="overflow-scroll ml-2 mr-2">
        <div class="hover:shadow-inner pt-1 pb-1 flex flex-row" v-for="(error, index) in resolved" :key="error.index">`{{ error.code }}` - {{ error.text }}
          <div class="w-8 cursor-pointer flex content-center mr-4">
            <button v-on:click="resolvedOnClick( index, resolvedBool )" class="text-2xl ">
              <img src="https://pics.freeicons.io/uploads/icons/png/19969543341557740370-512.png" alt="Send back to unresolved." />
            </button>
          </div>
        </div>

      </div>
    </div>

    <div class="tracking-wide pt-5 flex flex-col rounded-lg shadow-2xl w-1/4" style="backdrop-filter: blur(20px)">
      <h1 class=" text-2xl font-medium pb-5 flex justify-center">Unresolved</h1>
      <hr>
      <div class="overflow-scroll ml-2 mr-2">
        <div class="hover:shadow-inner pt-1 pb-1 flex flex-row" v-for="(error, index) in unresolved" :key="error.index">`{{ error.code }}` - {{ error.text }}
          <div class="w-8 cursor-pointer flex content-center mr-4">
            <button v-on:click="unresolvedOnClick( index )" class="text-2xl">
              <img src="https://pics.freeicons.io/uploads/icons/png/12567193451553167199-512.png" alt="Send to resolved." />
            </button>
          </div>
        </div>

      </div>
    </div>

    <div class="tracking-wide pt-5 flex flex-col rounded-lg shadow-2xl w-1/4" style="backdrop-filter: blur(20px)">
      <h1 class=" text-2xl font-medium pb-5 flex justify-center">Backlog</h1>
      <hr>
      <div class="overflow-scroll ml-2 mr-2">
        <div class="hover:shadow-inner pt-1 pb-1 flex flex-row" v-for="(error, index) in backlog" :key="error.index">`{{ error.code }}` - {{ error.text }}
          <div class="w-8 cursor-pointer flex content-center  mr-4">
            <button v-on:click="backlogOnClick( index )" class="text-2xl">
              <img  src="https://pics.freeicons.io/uploads/icons/png/1309748561553167201-512.png" alt="Send to  unresolved." />
            </button>
          </div>
        </div>

      </div>
    </div>

    </div>
  </div>
</template>

<script>



export default {
  async asyncData({ $axios }) {
    try {
      const { resolved, unresolved, backlog } = await $axios.$get(
        "http://localhost:8000/get_lists"
      );
      return {
        resolved,
        unresolved,
        backlog
      };
    } catch (error) {
      console.log(
        `Couldn't get error lists:\n${error}\nDid you start the API?`
      );
      console.log(
        "HINT: You can comment out the full `asyncData` method and work with mocked data for UI/UX development, if you want to."
      );
    }
  },
  data() {
    return {
      resolved: [],
      unresolved: [],
      backlog: [],
      // Added for Undo Button.
      resolvedBool: false,
      unresolvedBool: false,
      backlogBool: false
    };
  },
  
  methods: {
    
    // This was a little tricky, at first i tried to use error.index for each errors index but i had an issue:
    // If i would splice on item at index 0 it would work, 'delete' and then the item previously at index 1 would become 0
    // however, error.index would stay at 1 so if i clicked the item at 0 index it would delete the next one at index 1
    // figured that out by using a bunch of console.logs and decided to get my index from other source rather than
    // error.index, it seems to work now.
    resolvedOnClick(index) {
      this.unresolvedBool = false
      this.backlogBool = false
      // pushing the error to unresolved BEFORE removing it from resolved
      this.unresolved.push(this.resolved[index]);
      // error has been added to unresolved so i can now safely remove it from resolved.
      this.resolved.splice(index,1);
      // Trigger Bool in case Undo button will be used.
      this.resolvedBool = true
    },

    // Same as the previous onClick, except the other way.
    unresolvedOnClick(index) {
      this.resolvedBool = false
      this.backlogBool = false
      this.resolved.push(this.unresolved[index]);
      this.unresolved.splice(index,1);
      this.unresolvedBool = true
    },

    // Same logic as before except now we move error from backlog to Unresolved.
    backlogOnClick( index ) {
      this.unresolvedBool = false
      this.resolvedBool = false
      this.unresolved.push(this.backlog[index]);
      this.backlog.splice(index,1);
      this.backlogBool = true
    },
    // My logic for the undo button:
      // On line 85, 86, 87 i set up 3 booleans, whenever any of the onClick events fire, the boolean for that even will change to true
      // i do this so i know which action has been done LAST.The i simply use if statements to check for all 3 of them, if any one is true:
      // i am first reseting the boolean (probably that should be the last not first line in the if but its okay) then i pop out the last item into
      // lastItem and then i push lastItem in the array where it was previously.I realise this may be hacky and not the cleanest way but this is what i came up with:)
    undoOnClick() {
      if (this.resolvedBool == true) {
        let lastItem = this.unresolved.pop()
        this.resolved.push(lastItem)
        this.resolvedBool = false
  
      } 
      if (this.unresolvedBool == true) {
        let lastItem = this.resolved.pop()
        this.unresolved.push(lastItem)
        this.unresolvedBool = false
      } 
      if (this.backlogBool == true) {
        let lastItem = this.unresolved.pop()
        this.backlog.push(lastItem)
        this.backlogBool = false
      }
    }
  }
};
</script>
