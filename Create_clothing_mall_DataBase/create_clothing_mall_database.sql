-- # clothing_mall 데이터베이스(스키마) 생성
-- create database clothing_mall;

-- # clothing_mall로 포커싱, 사용
-- USE clothing_mall;

-- # product(상품) 테이블 생성
-- CREATE TABLE product (
--     product_id INT PRIMARY KEY,  						# 상품번호
--     gender VARCHAR(20),									# 남성/여성 옷 구분
--     master_category VARCHAR(50), 						# 상품 분류 (의류)
--     sub_category VARCHAR(50),    						# 상의/하의/속옷 등 구분
--     article_type VARCHAR(100),	 						# 옷 종류
--     base_colour VARCHAR(30),	 						    # 기본 색
--     season VARCHAR(20),  	     						# 계절
--     release_year YEAR,			 						# 출시년도
--     usage_type VARCHAR(50),		 						# 스타일, 용도
--     product_name VARCHAR(255)	 						# 상품이름
-- );

-- # 상품이름, 상품 분류 컬럼들 not null 제약 추가
-- alter table product modify column product_name VARCHAR(255) not null;  
-- alter table product modify column article_type varchar(100) not null;
-- alter table product modify column master_category varchar(50) not null;
-- alter table product modify column sub_category varchar(50) not null;

-- # product 테이블에 가격 컬럼 추가
-- alter table product add column price int not null check(price >= 0) default 0; 

-- # python과 mysql연결을 통해 21400개 데이터 삽입 확인
-- select count(*) from product;

-- # mall_member(쇼핑몰 회원) 테이블 생성
-- create table mall_member(
-- 	member_id int auto_increment primary key,			# 회원번호
-- 	login_id varchar(50) not null unique,				# 아이디
-- 	login_password varchar(255) not null,				# 비밀번호, 해시 값 저장 중요*
-- 	member_name varchar(50) not null,					# 회원이름
-- 	email varchar(100),									# 이메일
-- 	phone_number varchar(20),							# 전화번호
-- 	sign_up_date datetime default current_timestamp		# 가입일
-- );

-- # 회원 테이블의 가입일 컬럼 제약조건 수정
-- alter table mall_member modify column sign_up_date datetime not null;

-- # 회원 테이블의 이메일, 번호 컬럼 제약조건 수정
-- alter table mall_member modify email varchar(100) not null;
-- alter table mall_member modify phone_number	varchar(20) not null;
-- alter table mall_member add constraint unique(email);
-- alter table mall_member add constraint unique(phone_number);
-- select * from information_schema.table_constraints where constraint_schema = 'clothing_mall' and table_name = 'mall_member';

-- # product_option(상품 옵션) 테이블 생성
-- create table product_option(
-- 	option_id int auto_increment primary key,			    # 옵션번호
--     product_id int not null,							    # 상품번호
--     size varchar(20) not null,							# 사이즈
--     color varchar(30) not null,							# 색
--     stock int not null default 0,						# 재고

--     foreign key(product_id) references product(product_id)
-- );

-- #alter table product_option drop column color; # color 컬럼 삭제

-- # stock 컬럼 0 이상 제약조건 추가 및 (product_id, size) UNIQUE 제약 추가
-- alter table product_option add constraint check(stock >= 0);
-- alter table product_option add constraint unique(product_id, size);

-- # cart(장바구니) 테이블 생성
-- create table cart(
-- 	cart_number int auto_increment primary key,			    # 장바구니 번호
--     member_id int not null,								# 회원번호
--     option_id int not null,								# 옵션번호		
--     Quantity int not null check(Quantity >= 1),			# 수량

--     foreign key (member_id) references mall_member(member_id), 		
--     foreign key (option_id) references product_option(option_id),
--     unique(member_id, option_id)
-- );
--     
-- # product_order(주문) 테이블 생성
-- create table product_order(
-- 	order_id int auto_increment primary key,			    # 주문번호
--     member_id int not null,								# 회원번호
--     order_date datetime default current_timestamp,		# 주문일

--     foreign key (member_id) references mall_member(member_id)
-- );

-- # 주문 테이블 주문일 제약조건 추가
-- alter table product_order modify column order_date datetime not null;

-- # 주문 테이블 총 가격 컬럼 추가
-- alter table product_order add column total_price int not null default 0;
-- alter table product_order add constraint check(total_price >= 0);

-- # 주문번호 1번인 상품의 총 가격 업데이트
-- UPDATE product_order SET total_price = (SELECT SUM(unit_price * Quantity) FROM order_detail WHERE order_id = 1) WHERE order_id = 1;

-- # order_detail(주문세부) 테이블 생성
-- create table order_detail(
--     order_id int not null,								# 주문번호
--     option_id int not null,								# 옵션번호
--     Quantity int not null check(Quantity >= 1),			# 수량
--     
--     
--     foreign key (order_id) references product_order(order_id),
--     foreign key (option_id) references product_option(option_id),
--     primary key(order_id, option_id)
-- );

-- # 주문세부 테이블 개당 가격 컬럼 추가
-- alter table order_detail add column unit_price int not null check(unit_price >= 0); 

-- update product set price =    #가격 책정
-- 	case 
-- 		when article_type in ('Belts', 'Boxers', 'Bra', 'Briefs', 'Camisoles', 'Dupatta', 'Innerwear Vests', 'Leggings', 
-- 			'Lounge Shorts', 'Lounge Tshirts', 'Nightdress', 'Stockings', 'Suspenders', 'Tights', 'Tops', 'Trunk', 'Tshirts') then
-- 				5000 + floor(rand()*16) * 1000
-- 		when article_type in ('Baby Dolls', 'Bath Robe', 'Booties', 'Capris', 'Churidar', 'Dresses', 'Jeggings', 'Jumpsuit', 'Kurtas'
--         , 'Kurtis', 'Lounge Pants', 'Night suits', 'Patiala', 'Rain Trousers', 'Robe', 'Rompers', 'Salwar', 'Shapewear', 'Shirts'
--         , 'Shorts', 'Shrug', 'Skirts', 'Sweaters', 'Sweatshirts', 'Swimwear', 'Track Pants', 'Trousers', 'Tunics', 'Waistcoat') then
-- 				20000 + floor(rand()*21) * 1000
-- 		when article_type in ('Blazers', 'Clothing Set', 'Jackets', 'Jeans', 'Kurta Sets', 'Lehenga Choli', 'Nehru Jackets'
--         , 'Rain Jacket', 'Salwar and Dupatta', 'Sarees', 'Suits', 'Tracksuits') then
-- 				40000 + floor(rand()*41) * 1000
-- 	end
-- ;

-- create table wishlist(			# 찜 목록 테이블 생성
-- 	wishlist_id int auto_increment primary key,			# 찜 번호
-- 	member_id int not null,								# 회원번호
--     product_id int not null,							# 상품번호
--     
--     unique(member_id, product_id),
--     foreign key (member_id) references mall_member(member_id),
--     foreign key (product_id) references product(product_id)
-- );

-- create table review(			# 리뷰 테이블 생성
-- 	   review_id int auto_increment primary key,											# 리뷰번호
--     member_id int not null,																# 회원번호
--     product_id int not null,							   		 							# 상품번호
--     review_score decimal(2, 1) not null check (review_score between 0 and 5),			# 리뷰점수
--     review_content varchar(500),															# 리뷰내용
--     review_date datetime default current_timestamp,										# 리뷰일자	
--     
--     foreign key (member_id) references mall_member(member_id),
--     foreign key (product_id) references product(product_id),
--     unique(member_id, product_id)
-- );

-- # 리뷰점수 1에서 5점사이로 수정
-- alter table review drop constraint review_chk_1;
-- alter table review add constraint check (review_score between 1 and 5); 

-- # 리뷰일자 not null제약 추가
-- alter table review modify column review_date datetime not null default current_timestamp;

-- create table product_view(			# 조회 정보 테이블 생성
-- 	view_id int auto_increment primary key,					# 조회번호
--     member_id int,										# 회원번호(비회원가능)
--     product_id int not null,								# 상품번호
--     view_date datetime default current_timestamp,		# 조회일
--     
--     foreign key (member_id) references mall_member(member_id),
--     foreign key (product_id) references product(product_id)
-- );

-- # 조회일 not null 제약 추가
-- alter table product_view modify column view_date datetime not null default current_timestamp;

--  #사이즈 S/M/L/XL인 상품 삽입   83044개
-- insert into product_option(product_id, size, stock) select product.product_id, sizes.size, 10 + floor(rand()*41) 
-- from product 
-- cross join(select 'S' as size union	all select 'M' union all select 'L' union all select 'XL') as sizes
-- where product.article_type in ('Tshirts', 'Jackets', 'Shorts', 'Track Pants', 'Swimwear', 'Sweatshirts', 'Tops'
-- , 'Shirts', 'Capris', 'Dresses', 'Trousers', 'Skirts', 'Jeans', 'Bra', 'Leggings', 'Tunics', 'Kurtas'
-- , 'Lounge Pants', 'Sweaters', 'Waistcoat', 'Tracksuits', 'Churidar', 'Kurtis', 'Suits', 'Kurta Sets', 'Innerwear Vests'
-- , 'Lounge Shorts', 'Briefs', 'Trunk', 'Boxers', 'Shrug', 'Camisoles', 'Jeggings', 'Night suits', 'Blazers'
-- , 'Lehenga Choli', 'Salwar', 'Nehru Jackets', 'Patiala', 'Clothing Set', 'Jumpsuit', 'Rompers', 'Nightdress'
-- , 'Robe', 'Shapewear', 'Salwar and Dupatta', 'Baby Dolls', 'Rain Jacket', 'Rain Trousers', 'Lounge Tshirts'
-- , 'Bath Robe');

-- # 사이즈 Free인 상품 삽입   639개
-- insert into product_option(product_id, size, stock) select product.product_id, sizes.size, 10 + floor(rand()*41) 
-- from product 
-- cross join(select 'Free' as size) as sizes
-- where product.article_type in ('Dupatta', 'Sarees', 'Stockings', 'Tights', 'Belts', 'Suspenders', 'Booties');

-- 상품 이미지 테이블 생성
-- create table product_image (
-- 	image_id int auto_increment primary key,
-- 	product_id int not null,
--     image_url varchar(500) not null,
--     
--     foreign key (product_id) references product(product_id)
-- );
