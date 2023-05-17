<script setup>
import { onMounted } from 'vue';
import { useUserStore } from '~/stores/user';

const userStore = useUserStore()
const router = useRouter()
let jobs = ref()

onMounted(() => {
    if (!userStore.user.isAuthenticated) {
        router.push('/login')
    } else {
        getJobs()
    }
})

useSeoMeta({
    title: 'My jobs',
    ogTitle: 'My jobs',
    description: 'The description'
})

async function getJobs() {
    await $fetch('http://127.0.0.1:8080/api/v1/jobs/my-jobs/', {
        headers: {
            'Authorization': 'token ' + userStore.user.token,
            'Content-Type': 'application/json'
        },
    })
        .then(response => {
            jobs.value = response
        })
        .catch(error => {
            console.log('error', error)
        })
}

function deleteJob(id) {
    console.log('id', id)

    jobs.value = jobs.value.filter(job => job.id !== id)
}

</script>

<template>
    <div class="py-10 px-6">
        <h1 class="mb-6 text-2xl">My Jobs</h1>

        <div class="space-y-4">
            <Job v-for="job in jobs" :key="job.id" :job="job" :showButton="true" v-on:deleteJob="deleteJob(job.id)" />
        </div>
    </div>
</template>