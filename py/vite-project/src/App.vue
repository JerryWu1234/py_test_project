<template>
  <div class="container mx-auto p-4">
    <!-- 用户列表 -->
    <div class="mb-4">
      <button @click="showAddModal = true" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
        Add user
      </button>
    </div>
    <table class="table-auto w-full">
      <thead>
        <tr>
          <th class="px-4 py-2">Id</th>
          <th class="px-4 py-2">Name</th>
          <th class="px-4 py-2">Gender</th>
          <th class="px-4 py-2">Edit</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td class="border px-4 py-2">{{ user.id }}</td>
          <td class="border px-4 py-2">{{ user.name }}</td>
          <td class="border px-4 py-2">{{ user.gender }}</td>
          <td class="border px-4 py-2">
            <button @click="showEditUserModal(user)"
              class="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-1 px-2 rounded">
              Edit
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 分页控件 -->
    <div class="py-2">
      <button @click="changePage(page - 1)" :disabled="page <= 0"
        class="px-4 py-2 m-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400 disabled:opacity-50 disabled:cursor-not-allowed">
        <ChevronLeftIcon class="h-5 w-5" />
      </button>
      <span>Page {{ page + 1 }} of {{ totalPages }}</span>
      <button @click="changePage(page + 1)" :disabled="page >= totalPages - 1"
        class="px-4 py-2 m-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400 disabled:opacity-50 disabled:cursor-not-allowed">
        <ChevronRightIcon class="h-5 w-5" />
      </button>
      / total: {{ totalnumber }}
    </div>


    <!-- 编辑用户模态框 -->
    <div v-if="showAddModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3 text-center">
          <h3 class="text-lg leading-6 font-medium text-gray-900">Edit User</h3>
          <div class="mt-2 px-7 py-3">
            <input type="text" class="mb-3 px-4 py-2 border rounded-md w-full" placeholder="Name"
              v-model="editedUser.name">
            <select v-model="editedUser.gender" class="mb-3 px-4 py-2 border rounded-md w-full">
              <option disabled >Select Gender</option>
              <option>Male</option>
              <option>Female</option>
            </select>
          </div>
          <div class="items-center px-4 py-3">
            <button @click="showEditModal = false"
              class="px-4 py-2 bg-gray-500 text-white text-base font-medium rounded-md w-full shadow-sm hover:bg-gray-400">
              Cancel
            </button>
            <button @click="addUser()"
              class="px-4 py-2 bg-blue-500 text-white text-base font-medium rounded-md w-full shadow-sm hover:bg-blue-400 mt-3">
              Update
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/vue/20/solid'

export default {
  components: {
    ChevronLeftIcon,
    ChevronRightIcon
  },
  data() {
    return {
      users: [], // 用户数据应从后端获取
      showAddModal: false,
      totalPages: 0,
      page: 0,
      totalnumber: 0,
      per_page: 10,
      editedUser: {
        id: null,
        name: '',
        gender: ''
      },
    };
  },
  created() {
    this.getUserList(); // 组件加载时获取用户列表
  },
  methods: {
    showEditUserModal(user) {
      this.editedUser = Object.assign({}, user); // 复制用户数据到 editedUser
      this.showAddModal = true;
    },
    changePage(newPage) {
      if (newPage >= 0 && newPage < this.totalPages) {
        this.page = newPage;
        this.getUserList();
      }
    },
    // 获取用户列表
    getUserList() {
      // 使用 axios 或其他 HTTP 客户端从后端获取用户列表
      axios.get(`http://localhost:5000/get_user_list?page=${this.page}&per_page=${this.per_page}`)
        .then(response => {
          this.users = response.data.users;
          this.totalPages = response.data.pages;
          this.page = response.data.page;
          this.totalnumber = response.data.total;
        })
        .catch(error => {
          console.error("There was an error fetching the users: ", error);
        });
    },
    // 添加用户
    addUser() {
      if(this.editedUser.id) {
        this.updateUser();
        return;
      }
      // 使用 axios 或其他 HTTP 客户端发送数据到后端
      axios.post('http://localhost:5000/add_user', this.editedUser)
        .then(response => {
          // 处理响应，例如关闭模态框，清空 editedUser 对象，刷新用户列表等
          this.showAddModal = false;
          this.editedUser = { name: '', gender: '' };
          this.getUserList(); // 重新获取用户列表
        })
        .catch(error => {
          console.error("There was an error adding the user: ", error);
        });
    },
    // 编辑用户（需要在你的模板中绑定这个方法到编辑按钮）
    updateUser() {
      axios.put(`http://localhost:5000/edit_user/${this.editedUser.id}`, {
        name: this.editedUser.name,
        gender: this.editedUser.gender
      })
        .then(response => {
          this.showAddModal = false;
          this.getUserList(); // 刷新列表
        })
        .catch(error => {
          console.error("There was an error updating the user: ", error);
          // 处理错误情况
        });
    },
  }
};
</script>


<style lang="css"></style>
