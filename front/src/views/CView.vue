<template>
    <div class="tab">
        <div class="top" style="display: flex;
            justify-content: space-between">
            <el-input
                v-model="cno"
                :trigger-on-focus="false"
                clearable
                class="inline-input w-50"
                placeholder="😶‍🌫️请输入课程号，回车以查询"
                style="width: 20%;"
                @keyup.enter="search"
                />
            <el-switch
                v-model="dialogVisible"
                active-text="添加课程"
                @change="add"
                style="margin-right: 1%;"
            />
        </div>
        <el-table :data="tableData" stripe style="width: 100%"
            :defaylt-sort="{ prop: 'CNO', order: 'descending'}">
            <el-table-column prop="CNO" label="课程号" width="180" sortable />
            <el-table-column prop="CNAME" label="课程名" width="180" />
            <el-table-column prop="CSCORE" label="学分" sortable />
            <el-table-column align="right">
                <!-- 点击后弹出对话框，对话框接受当前行的参数 -->
                <template #default="scope">
                    <el-button size="small" type="warning" @click="handleEdit(scope.$index, scope.row)">Edit</el-button>
                    <el-button size="small" type="danger" @click="remove(scope.$index, scope.row)">Delete</el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
    <el-dialog title="条目信息" v-model="dialogVisible">
        <el-form :model="row_upd" label-width="80px">
            <el-form-item label="课程号">
                <el-input v-model="row_upd.CNO"  />
            </el-form-item>
            <el-form-item label="课程名">
                <el-input v-model="row_upd.CNAME"  />
            </el-form-item>
            <el-form-item label="学分">
                <el-input v-model="row_upd.CSCORE" />
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

interface INFO {
    CNO: string,
    CNAME: string,
    CSCORE: number,
}
const cno = ref('');
const index_upd = ref(-1);
const row_upd = ref<INFO>({
    CNO: '',
    CNAME: '',
    CSCORE: 0,
});

const dialogVisible = ref(false);

const add = () => {
    index_upd.value = -1;
}

const tableData = ref<INFO[]>([]);  
onMounted(() => {
    flash();
});

const flash = () => {
    axios.get('http://localhost:8010/api/c')
    .then((res) => {
        console.log(res);
        tableData.value = res.data;
    }).catch((err) => {
        console.log(err);
    });
}

const handleEdit = (index: number, row: JSON) => {
    row_upd.value = JSON.parse(JSON.stringify(row));
    index_upd.value = index;
    // 打开对话框
    dialogVisible.value = true;
}

const remove = (index: number, row: any) => {
    ElMessageBox.confirm('此操作将永久删除该条目，并且会删除 sc 表的相关数据, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
    }).then(() => {
        // 前端先删除
        axios.post('http://localhost:8010/api/c_del', {
            params: {
                cno: row.CNO,
            }
        }).then((res) => {
            if (res.data['status'] === 'failed') {
                ElMessage.error(res.data['msg']);
                return;
            }
            ElMessage.success('删除成功');
            flash();
        }).catch((err) => {
            console.log(err);
            ElMessage.error('删除失败');
        });
    }).catch(() => {
        ElMessage.info('已取消删除');
    });

}

const submmit = () => {
    dialogVisible.value = false;
    var url = 'http://localhost:8010/api/c_update';
    if (index_upd.value === -1) {
        // 插入而非修改
        url = 'http://localhost:8010/api/c_add';
    }
    var params = {
        old_cno: '',
        new_info: row_upd.value,
    };
    if (index_upd.value !== -1) {
        params.old_cno = tableData.value[index_upd.value].CNO;
    }

    axios.post(url, {
        params: params
    }).then((res) => {
        console.log(res);
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

const search = () => {
    console.log(cno.value);
    axios.post('http://localhost:8010/api/c', {
        params: {
            cno: cno.value,
        }
    }).then((res) => {
        console.log(res);
        if (res.data['status'] === 'failed') {
            ElMessage.error(res.data['msg']);
            return;
        }
        tableData.value = res.data;
    }).catch((err) => {
        console.log(err);
    });
}

</script>

<style scoped>
.tab {
    margin-top: 20px;
    /* 居中 */
    margin-left: 10%;
    margin-right: 10%;
}
.tab .top .dashed {
  border-top: 2px dashed var(--el-border-color);
}   
</style>
  