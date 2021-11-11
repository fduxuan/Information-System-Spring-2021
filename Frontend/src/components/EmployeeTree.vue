<template>
  <div>
    <div v-for="user in userData" :key="user.id" @click="$emit('handleUserSelected', user.id)">
      <a-row :class="`${user.id === selectedUser ? 'user-item-active' : ''} user-item`"
        type="flex" align="middle" justify="space-between">
        <a-avatar size="small" :src="require('../assets/avatar.webp')"  />
        <a-tooltip :title="user.name">
          <div class="text-one-line user-item-name">{{ user.name }}</div>
        </a-tooltip>

        <a-tooltip title="员工信息">
          <a-button class="user-item-btn" size="small" shape="circle" icon="edit" type="link" />
        </a-tooltip>
      </a-row>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EmployeeTree',
  props: {
    userData: {
      type: Array,
      default() { return [] },
    },
    selectedUser: {
      type: String,
      default() { return "1" },
    }
  }
}
</script>

<style scoped>
.user-item {
  background-color: white;
  border: 1px solid rgb(141, 178, 195);
  color: rgb(141, 178, 195);
  padding: 6px 15px;
  border-radius: 10px;
  width: 80%;
  font-weight: 600;
  margin-bottom: 15px;
  transition: width .3s, border-color .3s, color .3s, background-color .3s;
}

.user-item:hover,
.user-item-active {
  cursor: pointer;
  width: 92%;
  background-color: rgb(141, 178, 195);
  color: white;
  /* border-color: rgb(209, 156, 156); */
}

.user-item-name {
  flex: 1;
  margin-left: 8px;
  margin-right: 5px;
}

.user-item .user-item-btn {
  color: inherit;
  transition: color .1s;
}

.text-one-line {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

</style>