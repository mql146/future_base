# 以`python`为基础镜像
FROM python:3.9
# 暴露容器端口的声明
EXPOSE 8000
# 新建一个文件路径作为程序包工作路径
RUN mkdir -p /home/mql/Workspace/data/docker_img_ws/future_base_dimg
WORKDIR /home/mql/Workspace/data/docker_img_ws/future_base_dimg
# 复制项目内容到工作目录
COPY . /home/mql/Workspace/data/docker_img_ws/future_base_dimg
# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt
# 执行启动程序
CMD python /home/mql/Workspace/data/docker_img_ws/future_base_dimg/manage.py runserver 127.0.0.1:8000
