from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

import os

class AIResponse(models.Model):
    prompt = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    # 태그의 이름 (중복 불가)
    name = models.CharField(max_length=20, unique=True)
    # 태그의 고유 슬러그 (중복 불가, URL에 사용됨)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)    

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """
        태그의 고유 URL을 반환
        예: /blog/tag/파이썬-공부
        """
        return f'/blog/tag/{self.slug}'

# Category 모델: 블로그 글에 사용할 카테고리를 정의하는 모델
class Category(models.Model):
    # 카테고리 이름 (중복 불가)
    name = models.CharField(max_length=20, unique=True)
    # 카테고리의 고유 슬러그 (중복 불가, URL에 사용됨)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """
        카테고리의 고유 URL을 반환
        예: /blog/category/정치
        """
        return f'/blog/category/{self.slug}'

    class Meta:
        # 카테고리 모델의 복수형을 'Categories'로 설정
        verbose_name_plural = 'Categories'


class Post(models.Model):
    # 제목 (최대 30자)
    title = models.CharField(max_length=30)
    # 부제목 (최대 100자, 선택사항)
    hook_text = models.CharField(max_length=100, blank=True)

    # 콘텐츠는 Markdown 형식으로 작성
    content = MarkdownxField()
    # 이미지 업로드 필드 (폴더 구조: /blog/images/YYYY/MM/DD/)
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    # 파일 업로드 필드 (폴더 구조: /blog/files/YYYY/MM/DD/)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    # 생성일시 (자동 생성)
    created_at = models.DateTimeField(auto_now_add=True)
    # 수정일시 (수정 시 자동 갱신)
    updated_at = models.DateTimeField(auto_now=True)

    # 작성자 (User 모델과의 외래키 관계, 삭제 시 NULL로 설정)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # 카테고리 (Category 모델과의 외래키 관계, 선택사항, 삭제 시 NULL로 설정)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    # 태그 (Tag 모델과의 다대다 관계, 선택사항)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        """
        모델 인스턴스를 문자열로 출력할 때, [pk] 제목 :: 작성자 형태로 출력
        예: [1] 첫 번째 글 :: admin
        """
        return f'[{self.pk}] {self.title} :: {self.author}'
    
    def get_absolute_url(self):
        """
        게시물의 고유 URL을 반환
        예: /blog/1
        """
        return f'/blog/{self.pk}'

    def get_file_name(self):
        """
        업로드된 파일의 파일명을 반환
        """
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        """
        업로드된 파일의 확장자를 반환
        예: txt, pdf 등
        """
        return self.get_file_name().rsplit('.', maxsplit=1)[-1]

    def get_content_markdown(self):
        """
        Markdown 형식의 콘텐츠를 HTML로 변환하여 반환
        """
        return markdown(self.content)
