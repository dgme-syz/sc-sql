<template>
    <div class="tab">
        <el-row :span="24">
            <div style="width: 100%;display: flex;justify-content: left;">
                <el-col :span="3">
                    <el-input
                    v-model="sno_"
                    :trigger-on-focus="false"
                    clearable
                    class="inline-input w-50"
                    placeholder="🎨请输入学号"
                    />
                </el-col>
                <el-col :span="3" style="margin-left: 2%;">
                    <el-input
                    v-model="cno_"
                    :trigger-on-focus="false"
                    clearable
                    class="inline-input w-50"
                    placeholder="✨请输入课程号"
                    />
                </el-col>
                <!-- 查询按键靠最右边 -->
                <el-col :span="3" style="margin-left: auto;display: flex;">
                    <el-button type="primary" @click="add">添加</el-button>
                    <el-button type="primary" @click="search">查询</el-button>
                </el-col>
            </div>   
        </el-row>
        <el-row :span="24">
            <el-table :data="tableData" stripe style="width: 100%"
                :defaylt-sort="{ prop: 'SNO', order: 'descending'}">
                <el-table-column type="expand">
                    <template #default="props">
                    <div m="3">
                            <p m="t-0 b-2">学生姓名: {{ props.row.SNAME }}</p>
                            <p m="t-0 b-2">课程名称: {{ props.row.CNAME }}</p>
                            <p m="t-0 b-2">课程成绩:
                                <span :style="{ color: getColor(props.row.SSCORE) }"> {{ props.row.SSCORE }} </span>
                                {{ fun1(props.row.SSCORE) }} 
                            </p>
                    </div>
                    </template>
                </el-table-column>
                <el-table-column prop="SNO" label="学号" width="180" sortable />
                <el-table-column prop="CNO" label="课程号" width="180" />
                <el-table-column prop="CSCORE" label="课程学分" sortable />
                <el-table-column align="right">
                    <!-- 点击后弹出对话框，对话框接受当前行的参数 -->
                    <template #default="scope">
                        <el-button size="small" type="warning" @click="handleEdit(scope.$index, scope.row)">Edit</el-button>
                        <el-button size="small" type="danger" @click="remove(scope.$index, scope.row)">Delete</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-row>
    </div>  
    <!-- el-dialog 修改条目信息 -->
    <el-dialog title="修改条目信息" v-model="dialogVisible">
        <el-form :model="row_upd" label-width="80px">
            <el-form-item label="学号">
                <el-input v-model="row_upd.SNO"  />
            </el-form-item>
            <el-form-item label="课程号">
                <el-input v-model="row_upd.CNO"  />
            </el-form-item>
            <el-form-item label="课程成绩">
                <el-input v-model="row_upd.SSCORE" />
            </el-form-item>
        </el-form>
        <template #footer>
            <!-- 确定提交后将该信息送到后端 -->
            <el-button @click="dialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="submmit">确 定</el-button>
        </template>
    </el-dialog>
</template>
  
<script lang="ts" setup>
import axios from 'axios';
import { ref, onMounted} from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';


const index_upd = ref(-1);
const row_upd = ref({
    SNO: '',
    CNO: '',
    SSCORE: '',
});
const dialogVisible = ref(false);

const handleEdit = (index: number, row: JSON) => {
    console.log(index, row);
    row_upd.value = JSON.parse(JSON.stringify(row));
    index_upd.value = index;
    // 打开对话框
    dialogVisible.value = true;
}

const submmit = () => {
    dialogVisible.value = false;
    var url = 'http://localhost:8010/api/sc_update';
    if (index_upd.value === -1) {
        // 插入而非修改
        url = 'http://localhost:8010/api/sc_add';
    }
    var params = {
        old_sno: '',
        old_cno: '',
        sno: row_upd.value.SNO,
        cno: row_upd.value.CNO,
        sscore: row_upd.value.SSCORE,
    };
    if (index_upd.value !== -1) {
        params.old_sno = tableData.value[index_upd.value].SNO;
        params.old_cno = tableData.value[index_upd.value].CNO;
    }
    axios.post(url, {
        params: params
    }).then((res) => {
        if (res.data['status'] === 'failed') {
            ElMessage.error(res.data['msg']);
            return;
        }
        ElMessage.success('操作成功');
        dialogVisible.value = false;
        // 修改成功后刷新页面
        flash();
    }).catch((err) => {
        console.log(err);
        ElMessage.error('操作失败');
    });
}

const add = () => {
    console.log('add');
    // 打开对话框
    dialogVisible.value = true;
    row_upd.value = {
        SNO: '',
        CNO: '',
        SSCORE: '',
    };
    index_upd.value = -1;
}

const remove = (index: number, row: any) => {
    ElMessageBox.confirm('此操作将永久删除该条目, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
    }).then(() => {
        // 前端先删除
        axios.post('http://localhost:8010/api/sc_del', {
            params: {
                sno: row.SNO,
                cno: row.CNO,
            }
        }).then((res) => {
            tableData.value.splice(index, 1);
            ElMessage.success('删除成功');
            // 删除成功后刷新页面
            flash();
        }).catch((err) => {
            ElMessage.error('删除失败');
        });
    }).catch(() => {
        ElMessage.info('已取消删除');
    });

}

const flash = () => {
    axios.get('http://localhost:8010/api/sc')
    .then((res) => {
        console.log(res);
        tableData.value = res.data;
    }).catch((err) => {
        console.log(err);
    });
}

// 如果课程成绩大于90分，则在成绩后显示 good 否则显示 bad
const fun1 = (score: number) => {
    if (score >= 90) {
        return '😘';
    } else if (score >= 70) {
        return '😊';
    } else if (score >= 60) {
        return '😐';
    } else {
        return '😭';
    }
}
// 根据课程成绩显示不同的颜色
const getColor = (sscore: number) => {
    if (sscore >= 90) {
        return 'green';
    } else if (sscore >= 70) {
        return 'blue';
    } else if (sscore >= 60) {
        return 'yellow';
    } else {
        return 'red';
    }
}

// 查询学生信息
const sno_ = ref('');
const cno_ = ref('');
// 使用 axios 向后端发送请求，获得对应筛选后的数据
const search = () => {
    console.log(sno_.value, cno_.value);
    axios.post('http://localhost:8010/api/sc', {
        params: {
            sno: sno_.value,
            cno: cno_.value,
        }
    }).then((res) => {
        console.log(res);
        tableData.value = res.data;
    }).catch((err) => {
        console.log(err);
    });
}

// 进入页面立刻从后端获取数据
const tableData :any = ref([]);
onMounted(() => {
    flash();
});



</script>

<style scoped>
.tab {
    margin-top: 20px;
    /* 居中 */
    margin-left: 10%;
    margin-right: 10%;
}
</style>
  