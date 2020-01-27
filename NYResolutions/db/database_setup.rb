DataMapper.setup(:default, "sqlite://#{Dir.pwd}/db.sqlite")

class User
  include DataMapper::Resource

  property :id, Serial, key: true
  property :username, String, length: 128
  property :email, String, length: 128
  property :password, BCryptHash
  property :profile_id, Integer

  def authenticate(attempted_password)
    password == attempted_password
  end
end

class Profile
  include DataMapper::Resource

  property :id, Serial, key: true
  property :created_on, Date
  property :last_resolutions_update, Date

  has n, :resolutions
end

class Resolution
  include DataMapper::Resource

  property :id, Serial, key: true
  property :profile_id, Integer, required: true
  property :title, String, length: 128
  property :weekly_frequency, Integer
  property :activity_duration, Integer

  has n, :completions
  belongs_to :profile
end

class Completion
  include DataMapper::Resource

  property :id, Serial, key: true
  property :resolution_id, Integer, required: true
  property :activity_duration, Integer
  property :completed_on, Date

  belongs_to :resolution
end

DataMapper.finalize
DataMapper.auto_upgrade!
