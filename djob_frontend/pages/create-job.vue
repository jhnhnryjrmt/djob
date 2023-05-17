<script setup>
import { onMounted } from 'vue';
import { useUserStore } from '~/stores/user'

const userStore = useUserStore()
const router = useRouter()

onMounted(() => {
    if (!userStore.user.isAuthenticated) {
        router.push('/login')
    }
})

let { data: jobCategories } = await useFetch('http://127.0.0.1:8080/api/v1/jobs/categories/')

let category = ref('')
let title = ref('')
let description = ref('')
let position_salary = ref('')
let position_location = ref('')
let company_name = ref('')
let company_location = ref('')
let company_email = ref('')
let errors = ref([])

async function submitForm() {
    errors.value = []

    if (category.value == '') { errors.value.push('You must select a category') }
    if (title.value == '') { errors.value.push('Title field is empty') }
    if (description.value == '') { errors.value.push('Description field is empty') }
    if (position_salary.value == '') { errors.value.push('Salary field is empty') }
    if (position_location.value == '') { errors.value.push('Location field is empty') }
    if (company_name.value == '') { errors.value.push('Company Name field is empty') }
    if (company_location.value == '') { errors.value.push('Company Location field is empty') }
    if (company_email.value == '') { errors.value.push('Company Email field is empty') }

    if (errors.value.length == 0) {
        await $fetch('http://127.0.0.1:8080/api/v1/jobs/create-job/', {
            method: 'POST',
            headers: {
                'Authorization': 'token ' + userStore.user.token,
                'Content-Type': 'application/json'
            },
            body: {
                category: category.value,
                title: title.value,
                description: description.value,
                position_salary: position_salary.value,
                position_location: position_location.value,
                company_name: company_name.value,
                company_location: company_location.value,
                company_email: company_email.value
            }
        })
            .then(response => {
                console.log('response', response)

                router.push({ path: '/my-jobs' })
            })
            .catch(error => {
                if (error.response) {
                    for (const property in error.response._data) {
                        errors.value.push(`${property}: ${error.response._data[property]}`)
                    }
                    console.log(JSON.stringify(error.response))
                } else if (error.message) {
                    errors.value.push('Something went wrong. Please try again')

                    console.log(JSON.stringify(error))
                }
            })
    }
}
</script>

<template>
    <div class="py-10 px-6">
        <h1 class="mb-6 text-2xl">Create Job</h1>

        <form v-on:submit.prevent="submitForm" class="space-y-4">
            <div>
                <label>Category</label>
                <select v-model="category" class="w-full mt-2 p-4 rounded-xl bg-gray-100">
                    <option value="">Select Category</option>
                    <option 
                        v-for="category in jobCategories" 
                        v-bind:key="category.id" 
                        v-bind:value="category.id"
                    >
                        {{ category.title }}
                    </option>
                </select>
            </div>
            <div>
                <label>Title</label>
                <input v-model="title" type="text" class="w-full mt-2 p-4 rounded-xl bg-gray-100">
            </div>
            <div>
                <label>Description</label>
                <textarea v-model="description" type="text" class="w-full mt-2 p-4 rounded-xl bg-gray-100"></textarea>
            </div>
            <div>
                <label>Salary</label>
                <input v-model="position_salary" type="text" class="w-full mt-2 p-4 rounded-xl bg-gray-100">
            </div>
            <div>
                <label>Location</label>
                <input v-model="position_location" type="text" class="w-full mt-2 p-4 rounded-xl bg-gray-100">
            </div>
            <div>
                <label>Company Name</label>
                <input v-model="company_name" type="text" class="w-full mt-2 p-4 rounded-xl bg-gray-100">
            </div>
            <div>
                <label>Company Location</label>
                <input v-model="company_location" type="text" class="w-full mt-2 p-4 rounded-xl bg-gray-100">
            </div>
            <div>
                <label>Company E-mail</label>
                <input v-model="company_email" type="text" class="w-full mt-2 p-4 rounded-xl bg-gray-100">
            </div>

            <div v-if="errors.length" class="mb-6 py-4 px-6 bg-rose-400 text-white rounded-xl">
                <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
            </div>

            <button class="py-4 px-6 bg-teal-700 text-white rounded-xl">
                Submit
            </button>
        </form>
    </div>
</template>