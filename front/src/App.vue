<script>
import { onMounted, ref } from 'vue';
import axios from 'axios';

export default {
  setup() {
    
    // State
    const urlInput = ref('');
    const wordCountInput = ref('');
    const articleText = ref('');

    const showSummary = ref(false);
    const showErrorMessage = ref(false);
    const showWaitingMessage = ref(false);

    // Methods
    const submitText = () => {
      let url = urlInput.value;
      let wordCount = parseInt(wordCountInput.value);
      
      if (wordCountInput.value === '' || wordCountInput.value == 0) {
        wordCount = 400;
      }

      if (wordCount < 100) {
        wordCount = 100;
      }

      if (wordCount > 1000) {
        wordCount = 1000;
      }
      
      urlInput.value = '';
      wordCountInput.value = '';
      
      const urlPattern = /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/;
      let validURL = urlPattern.test(url);

      console.log('Text submitted:', url, 'Word count:', wordCount);
      console.log('Valid URL:', validURL);

      if(validURL) {
        showWaitingMessage.value = true;
        showSummary.value = false;
        showErrorMessage.value = false;

        axios.post('http://127.0.0.1:5000/generate', {
          url: url,
          word_count: wordCount
        }, {
          headers: {
            'Content-Type': 'application/json'
          },
          timeout: 60000,
        })
        .then(function (response) {
          console.log(response);
          articleText.value = response.data.summary;
          showSummary.value = true;
          showWaitingMessage.value = false;
        })
        .catch(function (error) {
          console.log(error);
        });
      } else {
        showErrorMessage.value = true;
      }
    };
    const filterNonNumeric = () => {
      // Remove non-numeric characters from the input
      wordCountInput.value = wordCountInput.value.replace(/\D/g, '');
    };

    return {
      submitText,
      filterNonNumeric,
      urlInput: urlInput,
      wordCountInput: wordCountInput,
      articleText: articleText,
      
      showSummary: showSummary,
      showErrorMessage: showErrorMessage,
      showWaitingMessage: showWaitingMessage,
    };
  },
};
</script>

<template>
  <div class="input-card">
    <h1 class="title">I don't wanna be here! corp.</h1>
    <div class="submit-box">
      <input id="url" v-model="urlInput" placeholder="Enter url..." />
      <input id="wcount" v-model="wordCountInput" placeholder="400" type="text" @input="filterNonNumeric"/>
      <button @click="submitText">Submit</button>
    </div>
    <span v-if="showErrorMessage" class="error-msg">Url is invalid</span>
    <span v-if="showWaitingMessage" class="wait-msg">Please wait...</span>
  </div>

  <div v-if="showSummary">
    <h2>Summary</h2>
    <p>{{ articleText }}</p>
  </div>
</template>

<style scoped>
.input-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  justify-self: center;
  align-self: center;

  margin-bottom: 50px
}

.title {
  color: #3498db; /* Blue accent color */
}

.submit-box {
  margin-top: 20px;
}

.error-msg {
  color: red;
  align-self: flex-start;
  margin-left: 8px;
  font-style: italic;
}

.wait-msg {
  color: #3498db; /* Blue accent color */
  align-self: flex-start;
  margin-left: 8px;
  font-style: italic;
}

#url {
  padding: 8px;
  margin-right: 8px;
  width: 40rem;
}

#wcount {
  padding: 8px;
  margin-right: 8px;
  width: 3.5rem;
  text-align: center;
}

button {
  padding: 8px 16px;
  background-color: #3498db; /* Blue accent color */
  color: #fff;
  border: none;
  cursor: pointer;
}

</style>
