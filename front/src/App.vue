<template>
    <el-header style="margin-top: 2%;">
        <el-text tag="b" style="font-size: 25px;">数据库选课管理系统</el-text>
    </el-header>
    <el-main>
        <el-tabs type="border-card" class="demo-tabs" style="margin-left: 2%;margin-right: 2%;">
        <el-tab-pane label="学生表"><SView/></el-tab-pane>
        <el-tab-pane label="课程表"><CView/></el-tab-pane>
        <el-tab-pane label="选课表"><HomeView/></el-tab-pane>
        </el-tabs>
    </el-main>
</template>

<script setup lang="ts">
import { Calendar } from '@element-plus/icons-vue'
import HomeView from './views/HomeView.vue'
import SView from './views/SView.vue'
import CView from './views/CView.vue'
// Define the type for ResizeObserverCallback if not available
type ResizeObserverCallback = (entries: ResizeObserverEntry[], observer: ResizeObserver) => void;

// Perfectly solve ResizeObserver loop limit exceeded issue
const debounce = (fn: (...args: any[]) => void, delay: number) => {
  let timer: ReturnType<typeof setTimeout> | null = null;
  return (...args: any[]) => {
    if (timer) {
      clearTimeout(timer);
    }
    timer = setTimeout(() => {
      fn(...args);
    }, delay);
  }
}

const _ResizeObserver = window.ResizeObserver;
window.ResizeObserver = class ResizeObserver extends _ResizeObserver {
  constructor(callback: ResizeObserverCallback) {
    const debouncedCallback = debounce(callback, 16);
    super(debouncedCallback as ResizeObserverCallback);
  }
}
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.demo-tabs .custom-tabs-label .el-icon {
  vertical-align: middle;
}
.demo-tabs .custom-tabs-label span {
  vertical-align: middle;
  margin-left: 4px;
}

.el-tabs--border-card>.el-tabs__header .el-tabs__item:not(.is-disabled):hover {
    color: #42b983 !important;
}
</style>
